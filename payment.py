from authenticate import authenticate_face

balance = 5000
amount = int(input("Enter Amount: "))

print("Face Authentication Required...")

if authenticate_face():
    if amount <= balance:
        balance -= amount
        print("Payment Successful")
        print("Remaining Balance:", balance)
    else:
        print("Insufficient Balance")
else:
    print("Payment Blocked - Face Not Verified")
