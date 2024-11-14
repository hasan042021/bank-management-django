# NexBank Project

NexBank is a banking system allowing users to manage their accounts, perform basic banking operations, and request loans.

## Features

### 1. **Create Account**

- Allows users to create a new bank account.
- Validations are required for user input (e.g., checking if user is already registered, ensuring valid account details).

### 2. **Report (Transactions History)**

- Displays all records of user transactions: deposits, withdrawals, and loan requests.
- **Report functionality**:
  - The report is dynamically updated as users perform transactions.
  - Information is retrieved from the database, sorted, and filtered by date .

### 3. **Deposit**

- Users can report deposits to their account balance.
- Restrictions on the deposit amount.

### 4. **Withdraw**

- Users can withdraw money from their account balance.
- Withdrawal must be less than or equal to the available account balance.
- The system prevents overdraft situations.
- Transactions recorded, and the balance updated accordingly.
- Withdrawal limits are imposed.

### 5. **Loan Request**

- Users can request a loan.
- **Complexities**:
  - Loan requests must be submitted with details such as amount, repayment period, etc.
  - All loan requests need **admin approval** before they are processed.
  - Admin must be able to review and approve or reject loan applications.
  - Loan status (pending, approved, rejected) should be visible to the user in their report.
  - Risks like handling credit scores and ensuring compliance with bank loan policies can be factors.

### 6. **Transfer Money**

- Users can transfer money to another user's account.
- **Complexities**:
  - Transfers can only be made to accounts that already exist in the system.
  - Transfer requests require the recipient’s account details (account number or user identifier).
  - The transaction must check if the user has sufficient balance to make the transfer.
  - Transaction is recorded and both accounts are updated accordingly.

## Additional Notes

- **User Authentication**: All users must be authenticated before performing transactions (e.g., login credentials).
- **Admin Role**: Admins have control over approving/rejecting loan requests and managing user accounts.
