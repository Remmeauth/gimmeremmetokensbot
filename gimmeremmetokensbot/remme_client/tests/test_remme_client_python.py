import sys
from unittest import *
from tests.test_remme_token import RemmeTokenTest


def main(argv):
    test_suite = TestSuite()

    if len(argv) > 0:
        for test_class in argv:
            test_class = eval(test_class)
            test_suite.addTest(makeSuite(test_class))
    else:
        test_suite.addTest(makeSuite(RemmeTokenTest))

    runner = TextTestRunner(stream=sys.stdout)
    result = runner.run(test_suite)

    if not result.wasSuccessful():
        sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
