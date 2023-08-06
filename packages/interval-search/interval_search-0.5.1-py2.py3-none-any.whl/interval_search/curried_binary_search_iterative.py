import typing


def curried_binary_search_iterative(
    predicate: typing.Callable[[int], bool],
    decorate_with: typing.Callable[[typing.Callable], typing.Callable] = lambda x: x,
) -> typing.Callable[[int, int], typing.Optional[int]]:
    """Find the positive integer threshold below which a search criteria is
    never satisfied and above which it is always satisfied.

    Currying allows for calls that don't pass the predicate callable
    as an argument, which is necessary for compatibility with Numba jit
    compilation.

    Parameters
    ----------
    predicate : callable object
        Returns whether an integer value satisfies the search criteria.
    decorate_with : callable, optional
        A decorator that will be applied to the inner search function. Useful
        to enable jit compilation.

    Returns
    -------
    searcher : Callable[[int, int], Optional[int]]
        The curried search function, which takes an optional integer
        `lower_bound` and `upper_bound` and returns the first integer value
        that satisfies the search criteria.

        If no value satisfies the search criteria, the search function
        will return None.
    """

    @decorate_with
    def binary_search_iterative(
        lower_bound: int,
        upper_bound: int,
    ) -> typing.Optional[int]:
        """Find the positive integer threshold below which a search criteria is
        never satisfied and above which it is always satisfied.

        Parameters
        ----------
        lower_bound : int
            Lower bound for the binary search, inclusive.
        upper_bound : int
            Upper bound for the binary search, inclusive.

        Returns
        -------
        guess
            The lowest integer value that satisfies the search criteria, and
            None if upper_bound does not satisfy the search criteria or search
            range is empty (i.e., lower_bound > upper_bound).
        """

        # Check if the range is invalid.
        if lower_bound > upper_bound:
            return None

        # Loop until lower_bound is greater than upper_bound
        while lower_bound <= upper_bound:
            # Find the midpoint
            midpoint = (lower_bound + upper_bound) >> 1  # equiv // 2

            # If predicate is satisfied by midpoint, search the left half.
            if predicate(midpoint):
                upper_bound = midpoint - 1
            # Otherwise, search the right half.
            else:
                lower_bound = midpoint + 1

        # If the search ended successfully, lower_bound is the answer.
        # Otherwise, return None.
        if predicate(lower_bound):
            return lower_bound
        else:
            return None

    return binary_search_iterative
