'''
J.Guanzon: Added a dropdown menu for the types of deduction that could be taken. 
'''

# Import required libraries
from numpy.core.records import record
import streamlit as st
from datetime import datetime
from dataclasses import dataclass
from typing import Any, List
import pandas as pd
import hashlib

# import
# Import required libraries
@dataclass
class RecordTransaction:
    amount: float
    type: str
    description: str
    receipt: str

# Our Block class
@dataclass
class Block:
    record: RecordTransaction
    trade_time: str = datetime.utcnow().strftime("%H:%M:%S")
    prev_hash: str = 0

    def hash_block(self):
        # Declare a hashing algorithm
        sha = hashlib.sha256()

        # Encode the time of trade
        trade_time_encoded = self.trade_time.encode()
        # Add the encoded trade time into the hash
        sha.update(trade_time_encoded)

        # Encode the Record class
        record = str(self.record).encode()
        # Then hash it
        sha.update(record)

        prev_hash = str(self.prev_hash).encode()
        sha.update(prev_hash)

        # Return the hash to the rest of the Block class
        return sha.hexdigest()

# Our StockChain class
from typing import List
@dataclass
class StockChain:
    # The class `StockChain` holds a list of blocks
    chain: List[Block]
    # The function `add_block` adds any new `block` to the `chain` list
    def add_block(self, block):
        self.chain += [block]

# Add text titles to the web page
st.markdown("# Write-Off Warrior Test")
st.markdown("## Enter Your Deductable Purchase Below:")

# Add an input area for the buyer


# Add an input area for the seller
type = st.selectbox(
    'Type of Deduction',
    ('Vehicle Expense', 'Educator Expense (max $250)', 'Employee Pay', 'Meals & Entertainment Expenses', 'Home Office Deduction')
)

description = st.text_input("Description of Purchase")
amount = st.text_input("Amount")

receipt = st.text_input("Receipt Hash")

# Set up the web app for deployment (including running the StockChain class)
@st.cache(allow_output_mutation=True)
def setup():
    genesis_block = Block(
        record=RecordTransaction(amount=0, type="N/a", description="N/A", receipt="N/A")
    )
    return StockChain([genesis_block])

# Serve the web app
stockchain_live = setup()

# Add a button using Streamlit to add a new block to the chain
if st.button("Add Block"):
    # Pull the original block to start on
    prev_block = stockchain_live.chain[-1]

    # Hash the original block (to put into the next block)
    prev_block_hash = prev_block.hash_block()

    # Create a `new_block` so that shares, buyer_id, and seller_id from the user input are recorded as a new block
    new_block = Block(
        # data=input_data,
        record=RecordTransaction(amount, type, description, receipt),
        prev_hash=prev_block_hash
    )

    # Add the new_block to the existing chain
    stockchain_live.add_block(new_block)

    # Just for fun, we add a little pizzazz
    st.balloons()

# Attempt a button to check shares
if st.button("Check Total Deductions"):
    total_deductions = 0.0
    for block in stockchain_live.chain:
        total_deductions += float(block.record.amount)
    st.write(total_deductions)

# Add a title for the chain display section
st.markdown("## The Stockchain Ledger")

# Save the data from the blockchain as a DataFrame
stockchain_df = pd.DataFrame(stockchain_live.chain)
# recs = stockchain_df
st.write(stockchain_df)

# stock_json = stockchain_df.to_json()

# st.text(stock_json[2])

# for element in stockchain_df:
#     st.text(element)
# Display the DataFrame data
# st.write(stockchain_df)
# st.write(Block.record.shares)

# Add a dropdown menu to allow users to select which block in the chain to display
st.sidebar.write("# Block Inspector")
selected_block = st.sidebar.selectbox(
    "Which block would you like to see?", stockchain_live.chain
)

# Display the selected block on the sidebar
st.sidebar.write(selected_block)