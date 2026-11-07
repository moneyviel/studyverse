"""Data shared by several units (the same business continues from unit to unit)."""
from lib import je


def kavya_entries():
    """Kavya Traders, April 2026 (Unit 1 illustration 1; posted in Unit 2, trial balance in Unit 3)."""
    return [
        je('Apr 1', [('Cash A/c', 400000)], [('Capital A/c', 400000)], 'Being business started with cash'),
        je('Apr 2', [('Bank A/c', 250000)], [('Cash A/c', 250000)], 'Being cash deposited to open a current account'),
        je('Apr 4', [('Purchases A/c', 72000)], [('Mehta & Co.', 72000)], 'Being goods bought on credit, list price ₹80,000 less 10% trade discount'),
        je('Apr 7', [('Rohan', 45000)], [('Sales A/c', 45000)], 'Being goods sold on credit'),
        je('Apr 10', [('Computer A/c', 38000)], [('Bank A/c', 38000)], 'Being office computer bought by cheque'),
        je('Apr 15', [('Mehta & Co.', 72000)], [('Bank A/c', 70560), ('Discount Received A/c', 1440)], 'Being amount due settled by cheque, 2% cash discount received'),
        je('Apr 18', [('Cash A/c', 44100), ('Discount Allowed A/c', 900)], [('Rohan', 45000)], 'Being cash received from Rohan in full settlement, 2% discount allowed'),
        je('Apr 22', [('Drawings A/c', 3500)], [('Purchases A/c', 3500)], 'Being goods taken by the proprietor for personal use'),
        je('Apr 25', [('Advertisement A/c', 2000)], [('Purchases A/c', 2000)], 'Being goods distributed as free samples'),
        je('Apr 30', [('Salaries A/c', 18000), ('Rent A/c', 12000)], [('Bank A/c', 30000)], 'Being salary and rent for April paid by cheque'),
    ]
