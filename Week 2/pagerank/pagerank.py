import os
import random
import re
import sys
from copy import deepcopy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # probability distribution of the next page to visit given current page
    next_page = dict()

    # pages the current page links to; if none, assume have one link to every page
    links = corpus[page]

    if not links:
        for p in corpus:
            links.add(p)

    # probability of choosing randomly from links in page
    p1 = damping_factor / len(links)

    # probability of choosing randomly from all pages
    p2 = (1 - damping_factor) / len(corpus)

    # assign each page to its probability of being visited next
    for webpage in corpus:
        if webpage in links:
            next_page[webpage] = p1 + p2
        else:
            next_page[webpage] = p2
    
    return next_page


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # PageRank values of all pages, found with sampling
    PageRanks = dict()

    # maps pages to respective dicts containing prob. dist. of which page to visit next
    next_page = dict()

    for page in corpus:
        # populate next_page dictionary
        next = transition_model(corpus, page, damping_factor)
        next_page[page] = next

        #initialise PageRanks dictionary
        PageRanks[page] = 0

    # first sample page randomly chosen
    page = ['']
    page[0] = random.choice(list(corpus))
    PageRanks[page[0]] += 1

    # subsequent samples
    for _ in range(n - 1):
        page = random.choices(list(next_page[page[0]]), weights = next_page[page[0]].values(), k=1)
        PageRanks[page[0]] += 1

    # calculate each page's sample proportion 
    for p in PageRanks:
        PageRanks[p] /= n

    return PageRanks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # PageRank values of all pages, they vary with each iteration
    PageRanks = dict()
    currentSet = dict()

    n = len(corpus)

    # initialise PR values
    for page in corpus:
        PageRanks[page] = 1 / n

        # a page without links is interpreted as having one link for every page
        if not corpus[page]:
            for p in corpus:
                corpus[page].add(p)

    # iterate until no PR value changes by more than 0.001
    while True:
        # get a copy of a set of current PR values
        currentSet = deepcopy(PageRanks)

        for page in PageRanks:
            sum = 0

            # get sum of PR(i)/NumLinks(i) for all i where 'i' is a page that links to page 'page'
            for link in PageRanks:
                if page in corpus[link]:
                    sum += currentSet[link] / len(corpus[link])

            # calculate new PR value for 'page'
            PageRanks[page] = (1 - damping_factor) / n + damping_factor * sum

        # condition to stop iteration
        stop = True

        for page in PageRanks:
            difference = abs(PageRanks[page] - currentSet[page])

            if difference > 0.001:
                stop = False
                break

        if stop:
            return PageRanks


if __name__ == "__main__":
    main()
