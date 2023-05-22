from flask import Flask,render_template,request
import json
import smtplib
from datetime import date

app = Flask(__name__)
with open('static/assets/recipes.json') as f:
    data = json.load(f)
all_posts=data
OWN_EMAIL = "erlangen.testing@gmail.com"
OWN_PASSWORD = "yfowwbynzizqfmco"


@app.route('/')
def get_app_posts():
    year = date.today().year
    return render_template("index.html",posts=all_posts, year=year)

@app.route("/about")
def about_page():
    return render_template("about.html")


@app.route("/contact",methods=["POST","GET"])
def contact_page():
    if request.method == 'POST':
        form_data = request.form
        if(form_data["u_name"]=="" or form_data["u_email"]=="" or form_data["u_tel"]=="" or  form_data["u_message"]==""):
            return render_template("contact.html", msg='plz fill the required fields and in correct format')
        else:
            send_email(form_data["u_name"],form_data["u_email"],form_data["u_tel"],form_data["u_message"])
            return render_template("contact.html",msg='Successfully sent your message')
    else:
        return render_template("contact.html")

def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    from_email=email
    print(from_email)
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(OWN_EMAIL,OWN_PASSWORD)
        connection.sendmail(OWN_EMAIL,OWN_EMAIL,email_message)
        connection.close()


@app.route("/post/<int:postid>")
def show_post(postid):
    requested_post = None
    for blog_post in all_posts:
        if blog_post["id"] == postid:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)



if __name__=='__main__':
    app.run(debug=True)