ID_no = input("Enter your ID: ")
print(ID_no[:5])
print(ID_no[-3])
print(ID_no[5:7])
print(ID_no[4:])
print(ID_no[::2])
email_no = input("Enter you mail: ")
index = email_no.index("@")
Username = email_no[:index]
Domain = email_no[index+1:]
print(f"Username: {Username}")
print(f"Domain: {Domain}")