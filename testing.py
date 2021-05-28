import unittest
from a_Naive import mandelbrot


class TestCase(unittest.TestCase):

    def setUp(self):
        pass

    def test_basic(self):
        """Test that c==0 always returns Max_iter"""

        c = complex(0, 0)

        for Max_iter in [0, 1, 2, 3, 4, 10, 20, 33, 45, 100]:
            count = mandelbrot(c,2, Max_iter)
            assert count == Max_iter

    def test_points_outside_set(self):

        for Max_iter in [1, 2, 3, 5, 10, 20, 100]:
            for c in [complex(5, 4), complex(2, 1), complex(-2, 1),
                      complex(2, -1), complex(-2, -1)]:
                count = mandelbrot(c,2, Max_iter)
                assert count == 1

    def test_arbitrary_points(self):
        for Max_iter in [10, 20, 100]:
            c = complex(1, 1.5)
            count = mandelbrot(c,2, Max_iter)
            assert count == 2

            c = complex(-1, 1.5)
            count = mandelbrot(c,2, Max_iter)
            assert count == 2

            c = complex(-1, -1.5)
            count = mandelbrot(c,2, Max_iter)
            assert count == 2

            c = complex(1, -1.5)
            count = mandelbrot(c,2, Max_iter)
            assert count == 2

            c = complex(1, 0)
            count = mandelbrot(c,2, Max_iter)
            assert count == 3

            c = complex(0.2, 1)
            count = mandelbrot(c,2, Max_iter)
            assert count == 4

            c = complex(0.2, 0.7)
            count = mandelbrot(c,2, Max_iter)
            assert count == 6

            c = complex(-0.2, 0.9)
            count = mandelbrot(c,2, Max_iter)
            assert count == 9

    def test_known_point(self):
        c = complex(0.5, 0.5)
        count = mandelbrot(c,2, 256)
        assert count == 5

    # -------------------------------------------------------------


if __name__ == "__main__":
    mysuite = unittest.makeSuite(TestCase, 'test')
    runner = unittest.TextTestRunner()
    runner.run(mysuite)
