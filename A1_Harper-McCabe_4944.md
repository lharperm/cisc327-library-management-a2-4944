### Liam Harper-McCabe
### 20394944
### Group 2

| Function Name | Implementation Status | What's Missing |
|---------------|-----------------------|----------------|
|'add_book_to_catalog'|Completed|N/A|
|'borrow_book_by_patron'|Completed|N/A|
|'return_book_by_patron'|Partially Complete|Missing all requirements for R4 
inlcuding patron ID and book ID parameters, verifying book borrower, updating available copies 
and return dates, and returning late fees owed|
|'calculate_late_fee_for_book'|Partially Complete|Missing requirements for R5 including calculating late fees
for overdue books (14 days late): $0.50/day for first 7 days overdue, $1.00/day for each additional day after 7 days, 
and a maximum of $15 per book. |
|'search_books_in_catalog'|Partially Complete|Missing R6 requirements including support for partial matching, exact matching, and returning results in same format as catelog display|
|'get_patron_status_report'|Partially Complete|Missing R7 requirements including displaying patron status that shows borrowed books, late fees owed, number of books borrowed, and borrowing history|

### Unit test summary

### Seperate test scripts were created for each function in the test directory. Each file contains 4-5 test statements that test 
### the requirements listed in requirements_specification.md. Tests were done using Pythons pytest package