import smtplib
from email.mime.text import MIMEText


# (*)���� ������ ����� ����
content = """
Test�Դϴ�
"""
title = '�׽�Ʈ�󱸿�'

msg = MIMEText(content)
msg['Subject'] = title

# (*)������ �߽��� ���� �ּ�, ������ ���� �ּ�, �ۺ�й�ȣ(�߽���) 
sender = 'nlb.thanks@gmail.com'
receiver = 'jangmankyu@hec.co.kr'
app_password = 'yice ygft mnhx nbtz'

# ���� ����
with smtplib.SMTP('smtp.gmail.com', 587) as s:
    s.starttls()

#????�α��� ������ ���� ������
    s.login(sender, app_password)
    s.sendmail(sender, receiver, msg.as_string())