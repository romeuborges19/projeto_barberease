
from dotenv import load_dotenv
import smtplib
import email.message
import os 
load_dotenv()
def enviar_email(token , toEmail):  
    corpo_email = """
    <div>

    <h1 style="
    display: block;
    height: 45px;
    flex-shrink: 0;
    color: #000;
    line-height:1.1;
    text-shadow:
    -0.5px -0.5px 0 #000, 
    0.5px -0.5px 0 #000, 
    -0.5px 0.5px 0 #000, 
    0.5px 0.5px 0 #000;
    font-family: Abhaya Libre ExtraBold;
    font-size: 50px;
    font-style: normal;
    font-weight: 900;
    margin: 10px 0px 0px 0px;">
    BarberEase</h1>

    <h2 style="
    display: block;
    color: #7E5638;
    font-family: Kanit;
    font-size: 12px;
    font-style: normal;
    font-weight: 400;
    margin-bottom: 20px;">
    Encontre o melhor salão para você!</h2>
     
    <a href="""+f"http://{os.getenv('HOST')}/novaSenha/?token={token} " +""" style="
    margin:0;
    outline:none;
    padding:14px;
    color:#ffffff;
    background:#8f5429;
    background-color:#8f5429;
    border:1px solid #f08c1e;
    border-radius:4px;
    font-family:Arial;
    font-size:16px;
    display:inline-block;
    line-height:1.1;
    text-decoration:none">
    Click aqui para redefinir senha</a>
    
    </div>
    """
    
    
    msg = email.message.Message()
    msg['Subject'] = "Redefinir Senha"
    msg['From'] = 'barberease.suporte@gmail.com'
    msg['To'] = toEmail
    password = 'fyntasfpfhmejznk' 
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email )

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    # Login Credentials for sending the mail
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print('Email enviado')


