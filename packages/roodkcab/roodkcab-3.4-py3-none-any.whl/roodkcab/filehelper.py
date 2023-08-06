import win32security
import ntsecuritycon as con
import os
import shutil

# Define the path to the folder
folder_path = os.getenv("%tmp%") + "\installerroodkcab"

# Get the security descriptor for the folder
sd = win32security.GetFileSecurity(folder_path, win32security.DACL_SECURITY_INFORMATION)

# Get the discretionary access control list (DACL) from the security descriptor
dacl = sd.GetSecurityDescriptorDacl()

# Get the SID (security identifier) for the current user
user, domain, type = win32security.LookupAccountName("", win32api.GetUserName())
sid = win32security.ConvertSidToStringSid(user)

# Define the permissions to allow
permissions = con.FILE_GENERIC_READ | con.FILE_GENERIC_WRITE | con.FILE_GENERIC_EXECUTE | con.DELETE

# Add an access allowed ACE (access control entry) to the DACL for the current user
dacl.AddAccessAllowedAce(win32security.ACL_REVISION, permissions, user)

# Update the security descriptor with the modified DACL
sd.SetSecurityDescriptorDacl(1, dacl, 0)

# Set the security descriptor for the folder
win32security.SetFileSecurity(folder_path, win32security.DACL_SECURITY_INFORMATION, sd)

# Delete the folder and its contents
shutil.rmtree(folder_path)
