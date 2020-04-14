# Welcome

This just contains some notes on the test data, to illustrate what is what and
how diversity is introduced. First of, all files are named after their edition and page.
If applicable, a filename consist of `<edition_id>_rating_<page>`

## Edition details

### The Dinner

`15797938-the-dinner` is an English edition with 82720 ratings. The number of reviews cannot be established.
In such a case, we will use ratings to extract the top 300 reviews per rating (and with text) from the edition.
This should amount to 1500 reviews. Pages in test data are some random samples, note that a page 10 is a last page.

Rating 5, page 1: A typical page with 30 reviews.

Rating 3, page 6: A typical page with 30 reviews.

Rating 1, page 10: A typical page with 30 reviews.

`22561799-het-diner` is a Dutch edition with just 7 ratings, 2 reviews.

Just one page with the 2 reviews, supplemented with the 5 ratings.

`9673614-la-cena` is an Italian edition with 104 text-only reviews (783 ratings).
This amounts to 4 pages of reviews. In test data, both the first and the last one are included.
No ratings used / needed here.
Interestingly, the last page of reviews does not include ratings on the page (as `22561799-het-diner` does).

### Harry Potter Sorcerer's stone

`28550610-harry-potter-and-the-sorcerer-s-stone` is an English edition with 1496 ratings. Number of reviews unknown.
Interestingly, there are not much reviews with a low rating. So, rating 5 gives a top 300, whereas lower ratings do not.

Rating 5, page 4: A typical page with 30 reviews.

Rating 5, page 10: The two very last reviews (i.e. with text), supplemented with 28 ratings.

Rating 2, page 1: Has only one 2 star rating (!), none with text. Is supplemented with first two ratings (to fill the width of a written review), and then a wild mix of reviews and ratings (4 and 5 stars)
