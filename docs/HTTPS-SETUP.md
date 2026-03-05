# HTTPS setup with Let's Encrypt

Do this **after** your app is running at http://YOUR_IP and you have a **domain** pointing to that IP.

---

## 1. Point your domain to the server

In your domain registrar (e.g. where you bought yourdomain.uz):

- Add an **A record**: host `@` (or your subdomain), value **20.233.1.20** (your Azure VM IP).
- Optionally add **www** → same IP or a CNAME to your main domain.

Wait a few minutes, then check: `ping yourdomain.uz` should show 20.233.1.20.

---

## 2. SSH into the server

```powershell
ssh -i C:\Users\USER\.ssh\id_ed25519 blogapp@20.233.1.20
```

---

## 3. Stop Nginx so Certbot can use port 80

```bash
cd ~/devops-blog
docker compose -f docker-compose.prod.yml stop nginx
```

---

## 4. Install Certbot and get the certificate

```bash
sudo apt update
sudo apt install -y certbot
sudo certbot certonly --standalone -d yourdomain.uz -d www.yourdomain.uz
```

Replace **yourdomain.uz** with your real domain. Use one `-d` if you only have the main domain.

- Enter your email when asked.
- Agree to the terms.
- When it succeeds, certs are in `/etc/letsencrypt/live/yourdomain.uz/`.

---

## 5. Create the Nginx SSL config on the server

Replace **yourdomain.uz** everywhere with your domain:

```bash
cd ~/devops-blog/nginx
cat > default.conf << 'NGINX_SSL'
upstream django {
    server web:8000;
}

server {
    listen 80;
    server_name yourdomain.uz www.yourdomain.uz;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    server_name yourdomain.uz www.yourdomain.uz;

    ssl_certificate /etc/letsencrypt/live/yourdomain.uz/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.uz/privkey.pem;

    location /static/ {
        alias /app/staticfiles/;
    }

    location /media/ {
        alias /app/media/;
    }

    location / {
        proxy_pass http://django;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
NGINX_SSL
sed -i 's/yourdomain.uz/YOUR_ACTUAL_DOMAIN/g' default.conf
```

**Important:** run this and replace **YOUR_ACTUAL_DOMAIN** with your domain (e.g. `mysite.uz`), or edit `default.conf` by hand and change every `yourdomain.uz` to your domain.

Example if your domain is `blog.uz`:

```bash
sed -i 's/yourdomain.uz/blog.uz/g' default.conf
```

---

## 6. Add your domain to Django ALLOWED_HOSTS

Edit the server `.env`:

```bash
cd ~/devops-blog
nano .env
```

Find the line with `DJANGO_ALLOWED_HOSTS` and add your domain (comma-separated), e.g.:

```
DJANGO_ALLOWED_HOSTS=20.233.1.20,localhost,127.0.0.1,yourdomain.uz,www.yourdomain.uz
```

Save (Ctrl+O, Enter, Ctrl+X).

---

## 7. Start Nginx again

```bash
docker compose -f docker-compose.prod.yml up -d nginx
```

---

## 8. Open the app over HTTPS

In the browser go to: **https://yourdomain.uz**

You should see the blog with a padlock. HTTP will redirect to HTTPS.

---

## 9. (Optional) Auto-renew certificates

Certbot can renew certs automatically. Add a cron job:

```bash
sudo crontab -e
```

Add this line (replace yourdomain.uz if needed):

```
0 3 * * * certbot renew --quiet --deploy-hook "cd /home/blogapp/devops-blog && docker compose -f docker-compose.prod.yml exec -T nginx nginx -s reload"
```

Or a simpler renewal (reload is optional):

```
0 3 * * * certbot renew --quiet
```

---

## Summary checklist

- [ ] Domain A record → 20.233.1.20  
- [ ] Stop nginx, run `certbot certonly --standalone -d yourdomain.uz`  
- [ ] Put SSL config in `~/devops-blog/nginx/default.conf` (replace yourdomain.uz)  
- [ ] Add domain to `DJANGO_ALLOWED_HOSTS` in `~/devops-blog/.env`  
- [ ] `docker compose up -d nginx`  
- [ ] Test https://yourdomain.uz  

**Note:** The CI/CD pipeline overwrites `nginx/default.conf` on each deploy. After you enable HTTPS, either keep a backup of your SSL `default.conf` and restore it after each deploy, or avoid re-copying the Nginx config in the workflow until you add a secret (e.g. `USE_SSL`) to deploy the SSL config automatically.
