# E - Commerce

EBay-like e-commerce auction site that allows users to post auction listings, place bids on listings, comment on those listings, and add listings to a “watchlist”

Developed using Python (Django), HTML, CSS (Bootstrap) and JavaScript

The data for auction listings, users and comments is stored in a SQL database 

The default route of the web application lets users view all of the currently active auction listings. Clicking on a listing takes the user to a page specific to that listing. On that page, users can view all details about the listing. Additionally, If the user is signed in, the user can add the item to their “Watchlist", bid on the item and leave a comment. If the user is the one who created the listing, the user has the ability to “close” the auction, which makes the highest bidder the winner of the auction and makes the listing no longer active. Users who are signed in can view their Watchlist page, Won Auctions and Lost Auctions. 
