import os
import random
import smtplib
import time
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()


def send_gmail(to_email, subject, html_body):
    sender_email = os.getenv("GMAIL_SENDER_EMAIL")
    app_password = os.getenv("GMAIL_SENDER_PASSWORD")

    msg = EmailMessage()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject
    msg["Reply-To"] = "no-reply@nowhere.com"

    msg.set_content("Please view this message in HTML format.")
    msg.add_alternative(html_body, subtype="html")

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(sender_email, app_password)
        smtp.send_message(msg)

    print(f"✅ Email sent successfully to {to_email}!")


def generate_sender_receiver_pairs(_emails):
    senders = _emails[:]
    receivers = _emails[:]

    while True:
        random.shuffle(senders)
        random.shuffle(receivers)
        # Ensure no one gifts themselves
        if all(s != r for s, r in zip(senders, receivers)):
            break

    return dict(zip(senders, receivers))


# def generate_html_message(sender_name, receiver_name):
#     return f"""
#     <html>
#     <body style="font-family: 'Segoe UI', Arial, sans-serif; background-color: #f7f7f7; padding: 20px;">
#         <div style="max-width: 600px; margin: auto; background: white; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); overflow: hidden;">
#             <div style="background-color: #e63946; color: white; text-align: center; padding: 16px 0;">
#                 <h1 style="margin: 0;">🎅 Secret Gift Exchange 🎁</h1>
#             </div>
#             <div style="padding: 24px; color: #333;">
#                 <p>Hi <strong>{sender_name}</strong>,</p>
#                 <p>It's time for our <strong>Secret Gift Exchange!</strong></p>
#                 <p style="font-size: 18px;">You’ve been chosen to give a gift to:</p>
#                 <div style="text-align: center; margin: 24px 0;">
#                     <div style="display: inline-block; padding: 16px 32px; border: 2px dashed #e63946; border-radius: 12px; background-color: #fff5f5; font-size: 20px; font-weight: bold; color: #e63946;">
#                         🎁 {receiver_name} 🎁
#                     </div>
#                 </div>
#                 <p>Please keep it secret — don’t tell anyone who you’re gifting to! 🤫</p>
#                 <p>Try to choose something thoughtful and have fun. ✨</p>
#                 <p style="margin-top: 40px;">Happy gifting,<br><strong>Secret Gift Exchange Organizer</strong></p>
#             </div>
#             <div style="background-color: #f1f1f1; text-align: center; padding: 12px; font-size: 12px; color: #777;">
#                 <p>Do not reply to this email. It was sent automatically.</p>
#             </div>
#         </div>
#     </body>
#     </html>
#     """

def generate_html_message(sender_name, reveal_link):
    return f"""
    <html>
    <body style="font-family: 'Segoe UI', Arial, sans-serif; background-color: #f7f7f7; padding: 20px;">
        <div style="max-width: 600px; margin: auto; background: white; border-radius: 16px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); overflow: hidden;">
            <div style="background-color: #e63946; color: white; text-align: center; padding: 16px 0;">
                <h1 style="margin: 0;">🎅 Secret Gift Exchange 🎁</h1>
            </div>
            <div style="padding: 24px; color: #333;">
                <p>Hi <strong>{sender_name}</strong>,</p>
                <p>It's time for our <strong>Secret Gift Exchange!</strong></p>
                <p style="font-size: 18px;">You’ve been chosen to give a gift to:</p>

                <!-- Scratch / Click-to-Reveal ticket -->
                <div style="text-align: center; margin: 24px 0;">
                    <a href="{reveal_link}" style="
                        display: inline-block;
                        padding: 16px 32px;
                        border: 2px dashed #e63946;
                        border-radius: 12px;
                        background-color: #c0c0c0;
                        font-size: 20px;
                        font-weight: bold;
                        color: #333;
                        text-decoration: none;
                    ">
                        🎁 Click to Reveal 🎁
                    </a>
                </div>

                <p>Click the ticket to see who you’ll be gifting to! 🤫</p>
                <p style="margin-top: 40px;">Happy gifting,<br><strong>Secret Gift Exchange Organizer</strong></p>
            </div>
            <div style="background-color: #f1f1f1; text-align: center; padding: 12px; font-size: 12px; color: #777;">
                <p>Do not reply to this email. It was sent automatically.</p>
            </div>
        </div>
    </body>
    </html>
    """


def generate_and_send_messages(_pairs, _users, send=False):
    for sender, receiver in _pairs.items():
        sender_name = _users[sender]
        receiver_name = _users[receiver]
        subject = "🎅 Your Secret Gift Exchange Match!"
        base_url = "https://kaloyan9905.github.io/new_year_gifts_generator/"
        reveal_link = f"{base_url}?user={receiver_name}"
        html_body = generate_html_message(sender_name, reveal_link)

        if send:
            send_gmail(sender, subject, html_body)
            time.sleep(1)  # To avoid hitting email sending limits
        else:
            print(f"--- Email preview for {sender} ---")
            print(html_body)
            print("-" * 60)


if __name__ == "__main__":
    # Example usage
    # emails = [
    #     "milchevkaloian@gmail.com",
    #     "krasi@gmail.com",
    #     "kati@gmail.com",
    #     "sasho@gmail.com",
    #     "viki@gmail.com",
    #     "buri@gmail.com"
    # ]

    emails = [
        "milchevkaloian@gmail.com",
        "krasimirowichh2005@gmail.com",
        "jordanovakatrin@gmail.com",
    ]

    users = {
        "milchevkaloian@gmail.com": "Koko",
        "krasimirowichh2005@gmail.com": "Krasi",
        "jordanovakatrin@gmail.com": "Kati"
    }

    # users = {
    #     "milchevkaloian@gmail.com": "Koko",
    #     "krasi@gmail.com": "Krasi",
    #     "kati@gmail.com": "Kati",
    #     "sasho@gmail.com": "Sasho",
    #     "viki@gmail.com": "Viki",
    #     "buri@gmail.com": "Buri"
    # }

    pairs = generate_sender_receiver_pairs(emails)
    generate_and_send_messages(pairs, users, send=True)  # change to True to send
