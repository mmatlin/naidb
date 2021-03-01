from naidb import __version__
from naidb import interpreter
from naidb.lexer import NaiDBLexer


def test_version():
    assert __version__ == "0.1.0"


def test_basic():
    # "test" should parse to a NAME and expression_terminator without issue
    assert interpreter.execute_string("test")


def test_syntax_prototype_lexes():
    lexer = NaiDBLexer()
    # Testing that *very* early syntax lexes without raising an exception
    lexer.input_(
        """\
let ne_voc_students =
    {schools:students}                                                        // inner join
    [#.1.name == #.2.school_name]                                             // on school name
    [#.1.region == "northeast" and #.1.type == "vocational"]                  // filtering further
    (#.2.first_name, #.2.last_name, #.1.school_name)                          // selecting output columns
in
    print_rows(ne_voc_students)                                               // prints out ne_voc_students
    print_rows(ne_voc_students(concat(str(.1), " ", str(.2), ": ", str(.3)))) // prints out ne_voc_students but a bit fancier"""
    )
    lexer.get_tokens()


def test_syntax_prototype_parses():
    # Testing that a testcase made with early syntax lexes/parses without raising an exception
    interpreter.execute_string(
        """\
// Set current schema to be "testing"
Environment.set(.schema, "testing");
import(naidb.Trigger, "Trigger");"""
    )
