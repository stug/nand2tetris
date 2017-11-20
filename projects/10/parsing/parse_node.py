"""This is my attempt at a fairly general parsing framework that could be used
to generate a parser from a description of the Jack grammar.  It has some good
ideas, but may be too fancy.

The basic premise is that we are building a parse tree out of ParseNodes, each
of which must implement an attempt_parse method.  The parse nodes pass around
a TokenProxy object, which keeps track of our position in a stream of tokens.
When a parse node starts, it saves the current position in the stream of tokens
so that if it fails, we can backtrack and try something else.  This mostly
works, although see the note in jack_non_terminals.py about the ordering of
child nodes for the Term parse node class.

Non-terminal parse nodes are just collections of other parse nodes whose job is
mainly to delegate parsing to their children and implement some error handling.
Terminal parse nodes actually look at the tokens and advance us in the token
stream.  There are also some ParseNode generator methods to implement the
`any_of`, `zero_or_more`, and `optional` node wrappers.

See jack_non_terminals.py for an example of how this is used.

I am leaving this for now since it feels like about as deep into parsing as I'd
like to go for now, but some ideas for the future:

* Try to do some pre-processing of the tree so that we can be smarter about
which of the possible branches to try first.  More or less, each node could
determine the first terminal node it would would end up checking for each of
its possible branches.  Then it could peek at the next token and decide which
branch to take.  In some cases (for non LL1 grammars) two branches might have
the same first terminal node, in which case it could look at each of those
branches' second terminal node, and so on -- this would let us be smarter and
handle (I think) any LL grammar?  Would need to be careful about optional nodes
in the parse tree, though.
* Separate the parse tree from the generated syntax tree -- some of the issues
I encountered here are due to the differing state requirements of those two
concerns.  ALSO this would make it so that the compilation logic doesn't need
to know about the syntax (currently it needs to know, e.g., that a function's
return type is the 2nd word in a function definition
* Look into parser combinators, says Julian from RC :)
"""
from parsing.token_proxy import TokensExhaustedException


class ParseException(Exception): pass


class ParseNode:

    grammar_element_name = None  # name of this element in the grammar

    def attempt_parse(self, token_proxy):
        saved_token_position = token_proxy.current_token_position

        # print('\n{} attempting to parse {}, token #{}'.format(
        #     self.node_type_name(),
        #     token_proxy.get_current_token(),
        #     token_proxy.current_token_position,
        # ))

        try:
            successful_node = self.parse(token_proxy)
            # print('  {} succeeded parsing {}, token #{}'.format(
            #     self.node_type_name(),
            #     token_proxy._tokens[saved_token_position],
            #     saved_token_position,
            # ))
            return successful_node
        except ParseException as e:
            # since we've failed to parse, reset the token stream to its
            # previous state
            token_proxy.set_token_position(saved_token_position)
            # print('  {} failed parsing {}, token position reset to {}'.format(
            #     self.node_type_name(),
            #     token_proxy._tokens[saved_token_position],
            #     saved_token_position,
            # ))
            raise

    def parse(self, token_proxy):
        """Should attempt to parse the token stream and raise a ParseException
        if it cannot.  Returns an instance of the class if parsing succeeds.
        """
        raise NotImplementedError

    # for use in error messages
    @classmethod
    def node_type_name(cls):
        return cls.__name__


class NonTerminalParseNode(ParseNode):
    """A parse node made up of other parse nodes"""
    
    # subclasses should override this
    child_node_types = []

    def __init__(self):
        self.child_nodes = []

    def parse(self, token_proxy):
        for child_node_type in self.child_node_types:
            child_node = child_node_type().attempt_parse(token_proxy)

            # TODO: this is a bit of a hack to make zero_or_more work :-/
            if isinstance(child_node, list):
                self.child_nodes.extend(child_node)
            else:
                self.child_nodes.append(child_node)

        return self


class BaseAnyOf(ParseNode):
    """Try a bunch of different ParseNodes"""
    allowed_node_types = None

    def attempt_parse(self, token_proxy):
        # TODO: instead of this could go down the tree to find all possible 
        # beginning terminals to determine where to go next?

        # print('\n{} attempting to parse {}, token #{}'.format(
        #     self.node_type_name(),
        #     token_proxy.get_current_token(),
        #     token_proxy.current_token_position,
        # ))

        for node_type in self.allowed_node_types:
            try:
                successful_parse = node_type().attempt_parse(token_proxy)
                # print('  {} succeeded!'.format(self.node_type_name()))
                return successful_parse
            except ParseException as e:
                pass

        raise ParseException('Expected one of the following: {}, got {}'.format(
            [node_type.node_type_name() for node_type in self.allowed_node_types],
            token_proxy.get_current_token(),
        ))


def any_of(allowed_node_types):
    class GeneratedAnyOf(BaseAnyOf): pass
    GeneratedAnyOf.allowed_node_types = allowed_node_types

    return GeneratedAnyOf


class BaseZeroOrMore(ParseNode):

    node_type_sequence = None

    def attempt_parse(self, token_proxy):
        # print('\n{} attempting to parse {}, token #{}'.format(
        #     self.node_type_name(),
        #     token_proxy.get_current_token(),
        #     token_proxy.current_token_position,
        # ))

        nodes = []
        while True:
            try:
                nodes_to_add = [
                    node_type().attempt_parse(token_proxy)
                    for node_type in self.node_type_sequence
                ]
            except ParseException:
                break
            else:
                nodes.extend(nodes_to_add)
        return nodes


def zero_or_more(node_type_sequence):
    class GeneratedZeroOrMore(BaseZeroOrMore): pass
    GeneratedZeroOrMore.node_type_sequence = node_type_sequence

    return GeneratedZeroOrMore


class BaseOptional(NonTerminalParseNode):

    child_node_types = None

    def attempt_parse(self, token_proxy):
        saved_token_position = token_proxy.current_token_position

        try:
            self.parse(token_proxy)
            return self.child_nodes  # don't want an Optional node in the tree
        except ParseException as e:
            # since we've failed to parse, reset the token stream to its
            # previous state
            token_proxy.set_token_position(saved_token_position)

            # need to return an empty list because containing non-terminal will
            # add out return value to its list of nodes
            return []


def optional(node_type_sequence):
    class GeneratedOptional(BaseOptional):
        child_node_types = node_type_sequence

    return GeneratedOptional
        

class TerminalParseNode(ParseNode):
    """Wraps an actual token"""

    def __init__(self):
        self.token = None

    def parse(self, token_proxy):
        token = token_proxy.get_next_token()
        return self.parse_token(token)

    def parse_token(self, token):
        """Expected to parse a single token, raise a ParseException if it can't
        and otherwise save the token and return self
        """
        raise NotImplementedError
