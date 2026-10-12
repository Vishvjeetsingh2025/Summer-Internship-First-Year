import csv
import smtplib
import ssl
import certifi  # Fixes CERTIFICATE_VERIFY_FAILED errors on Windows


def run_notification_engine(data_source_csv, sender_account, account_token):
    # Defining network host properties for a standard mail server
    smtp_distribution_server = "smtp.gmail.com"
    secure_port = 465  # Standard port for SSL network streams

    # Message structural blueprint with matching variable anchor keys
    notification_template = """Subject: Urgent Academic Update: Lab Pending Requirements

Dear {candidate_name},

This is an automated notification tracking system message regarding your technical records. Our internal logs show an outstanding submission status for your recent course modules.

Please ensure that your files are uploaded before the upcoming university evaluation cycle.

Best Regards,
Academic Coordination Office
"""

    print("[INFO] Initiating network layer setup...")
    # Creating a secure context container to enforce transport encryption
    # Using certifi's certificate bundle instead of the OS default store
    # fixes the "Basic Constraints of CA cert not marked critical" error
    # that occurs on some Windows machines.
    encryption_context = ssl.create_default_context(cafile=certifi.where())

    try:
        # Opening the local contact storage registry file
        print(f"[INFO] Reading student contact records from: {data_source_csv}")
        with open(data_source_csv, mode='r', encoding='utf-8-sig') as registry_file:
            data_reader = csv.reader(registry_file)
            header = next(data_reader)  # Skipping column title row

            # Establish an active network connection stream with the mail relay host
            print(f"[INFO] Linking to mail distribution server: {smtp_distribution_server}")
            with smtplib.SMTP_SSL(smtp_distribution_server, secure_port, context=encryption_context) as network_pipe:

                # Authenticate application profile on the remote host system
                network_pipe.login(sender_account, account_token)
                print("[SUCCESS] Server verification passed. Commencing loop execution...")

                # Iterate through individual rows in the contact file
                for row in data_reader:
                    if not row or len(row) < 2:
                        continue  # Skip blank/malformed rows

                    recipient_name = row[0].strip()
                    recipient_email = row[1].strip()

                    # Logic Step: Inject raw variables into the template anchors
                    personalized_message = notification_template.format(
                        candidate_name=recipient_name
                    )

                    # Network Step: Dispatch the compiled message block across the socket
                    network_pipe.sendmail(sender_account, recipient_email, personalized_message)
                    print(f"[LOG] Notification successfully pushed to: {recipient_name} ({recipient_email})")

        print("\n[SUCCESS] Notification pipeline completed all tasks without errors.")

    except FileNotFoundError:
        print("[ERROR] Could not read records. Target data sheet was not found.")
    except smtplib.SMTPAuthenticationError:
        print("[ERROR] Server login rejected. Check account credentials or access tokens.")
    except ssl.SSLCertVerificationError as ssl_err:
        print(f"[ERROR] SSL certificate verification failed: {ssl_err}")
        print("[HINT] Try running: pip install --upgrade certifi")
    except Exception as error_msg:
        print(f"[SYSTEM FAILURE] Transmission pipeline halted: {str(error_msg)}")


# --- Operational Setup Example for Testing ---
data_file = "student_directory.csv"          # Expects columns: Name, Email
admin_user = "freeusefree377847374@gmail.com"       # Your Gmail address
admin_app_key = "jsfjhsdjkfhsdjhfjkdshfjk"        # 16-character Gmail App Password

run_notification_engine(data_file, admin_user, admin_app_key)