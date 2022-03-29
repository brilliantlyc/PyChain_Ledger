# PyChain Ledger
################################################################################

# Step 1: Create a Record Data Class
# * Create a new data class named `Record`. This class will serve as the
# blueprint for the financial transaction records that the blocks of the ledger
# will store.

# Step 2: Modify the Existing Block Data Class to Store Record Data
# * Change the existing `Block` data class by replacing the generic `data`
# attribute with a `record` attribute that’s of type `Record`.

# Step 3: Add Relevant User Inputs to the Streamlit Interface
# * Create additional user input areas in the Streamlit application. These
# input areas will collect the relevant information for each financial record
# that will be stored in the `PyChain` ledger.

# Step 4: Test the PyChain Ledger by Storing Records
# * Test the complete `PyChain` ledger.

################################################################################
# Imports
import streamlit as st
from dataclasses import dataclass
from typing import Any, List
import datetime as datetime
import pandas as pd
import hashlib

################################################################################
# Step 1:
# Create a Record Data Class
# This new `Record` class will be used as the data type of the `record` attribute in the next section.

# Create a Record Data Class that consists of the `sender`, `receiver`, and
# `amount` attributes
@dataclass
class Record:
    sender: str
    receiver: str
    amount: float



################################################################################
# Step 2:
# Modify the Existing Block Data Class to Store Record Data


@dataclass
class Block:

    # Rename the `data` attribute to `record`, and set the data type to `Record`
    record: Record

    creator_id: int
    prev_hash: str = "0"
    timestamp: str = datetime.datetime.utcnow().strftime("%H:%M:%S")
    nonce: int = 0

    # Define the function that hashes the block
    def hash_block(self):
        sha = hashlib.sha256()

        record = str(self.record).encode()
        sha.update(record)

        creator_id = str(self.creator_id).encode()
        sha.update(creator_id)

        timestamp = str(self.timestamp).encode()
        sha.update(timestamp)

        prev_hash = str(self.prev_hash).encode()
        sha.update(prev_hash)

        nonce = str(self.nonce).encode()
        sha.update(nonce)

        return sha.hexdigest()


# Define the PyChain data class which consists of a chained list of blocks and a difficulty for proof of work
@dataclass
class PyChain:
    chain: List[Block]
    difficulty: int = 4

    # Define proof of work funtion using difficulty of the PyChain instance
    def proof_of_work(self, block):

        calculated_hash = block.hash_block()

        num_of_zeros = "0" * self.difficulty

        while not calculated_hash.startswith(num_of_zeros):

            block.nonce += 1

            calculated_hash = block.hash_block()

        print("Winning Hash", calculated_hash)
        return block

    # Define function that adds a block to the PyChain by first performing proof of work
    def add_block(self, candidate_block):
        block = self.proof_of_work(candidate_block)
        self.chain += [block]

    # Define function that validates the blockchain by checking if each block's prev_hash is in fact  
    # the hash of the previous block
    def is_valid(self):
        block_hash = self.chain[0].hash_block()

        for block in self.chain[1:]:
            if block_hash != block.prev_hash:
                print("Blockchain is invalid!")
                return False

            block_hash = block.hash_block()

        print("Blockchain is Valid")
        return True

################################################################################
# Streamlit Code

# Adds the cache decorator for Streamlit


@st.cache(allow_output_mutation=True)
def setup():
    print("Initializing Chain")
    return PyChain([Block("Genesis", 0)])


st.markdown("# PyChain")
st.markdown("## Store a Transaction Record in the PyChain")

pychain = setup()

################################################################################
# Step 3:
# Add Relevant User Inputs to the Streamlit Interface

# Code additional input areas for the user interface of the Streamlit
# application. Create these input areas to capture the sender, receiver, and
# amount for each transaction that will be stored in the `Block` record.


# Delete the `input_data` variable from the Streamlit interface.

# Add an input area where you can get a value for `sender` from the user.
input_sender = st.text_input("Sender")

# Add an input area where you can get a value for `receiver` from the user.
input_receiver = st.text_input("Receiver")

# Add an input area where you can get a value for `amount` from the user.
input_amount = st.text_input("Amount")

if st.button("Add Block"):
    # prev_block is the last block in the 'chain' list attribute of the pychain
    prev_block = pychain.chain[-1]
    prev_block_hash = prev_block.hash_block()

    # Update `new_block` so that `Block` consists of an attribute named `record`
    # which is set equal to a `Record` that contains the `sender`, `receiver`,
    # and `amount` values
    # Create a new variable 'input_record' to hold the 'Record'
    input_record=Record(sender=input_sender, receiver=input_receiver, amount=float(input_amount))
    new_block = Block(
        record=input_record,
        creator_id=42,
        prev_hash=prev_block_hash
    )

    pychain.add_block(new_block)
    st.balloons()

################################################################################
# Streamlit Code (continues)

st.markdown("## The PyChain Ledger")

# Create a DataFrame from the pychain (blockchain) and display it on the streamlit interface
pychain_df = pd.DataFrame(pychain.chain).astype(str)
st.write(pychain_df)

# Add a sidebar slider that allows the user to change the hashing difficulty for the proof of work
# when adding a new block (transaction) to the pychain
difficulty = st.sidebar.slider("Block Difficulty", 1, 5, 2)
pychain.difficulty = difficulty

# Add a sidebar selectbox that allows the user to inspect (look at the details of) a specific block from the pychain
st.sidebar.write("# Block Inspector")
selected_block = st.sidebar.selectbox(
    "Which block would you like to see?", pychain.chain
)

st.sidebar.write(selected_block)

# Add a button that displays if the pychain is valid 
# It displays True or False
if st.button("Validate Chain"):
    st.write(pychain.is_valid())

################################################################################
# Step 4:
# Test the PyChain Ledger by Storing Records

# Test the complete `PyChain` ledger and user interface by running the
# Streamlit application and storing some mined blocks in the `PyChain` ledger.
# Then test the blockchain validation process by using the `PyChain` ledger.
# To do so, complete the following steps:

# 1. In the terminal, navigate to the project folder where this pychain.py file exists

# 2. In the terminal, run the Streamlit application by
# using `streamlit run pychain.py`.

# 3. Enter values for the sender, receiver, and amount, and then click the "Add
# Block" button. Do this several times to store several blocks in the ledger.

# 4. Verify the block contents and hashes in the Streamlit drop-down menu.

# 5. Test the blockchain validation process by using the web interface.

