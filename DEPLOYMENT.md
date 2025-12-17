# Deployment Guide

This guide covers deploying the Library Management System to production.

## 🚀 Deployment Options

### Option 1: Docker Compose (Recommended for VPS)

#### Prerequisites
- Ubuntu 20.04+ or similar Linux server
- Docker and Docker Compose installed
- Domain name (optional but recommended)
- SSL certificate (Let's Encrypt recommended)

#### Steps

1. **Prepare Server**
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

2. **Clone Repository**
```bash
cd /opt
sudo git clone <repository-url> library_management
cd library_management
```

3. **Configure Environment**
```bash
# Backend environment
cat > server/.env << EOF
DEBUG=False
SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com,your-server-ip
DB_ENGINE=django.db.backends.mysql
DB_NAME=library_db
DB_USER=library_user
DB_PASSWORD=STRONG_PASSWORD_HERE
DB_HOST=db
DB_PORT=3306
EOF

# Update docker-compose.yml with strong passwords
```

4. **Start Services**
```bash
sudo docker-compose up -d
```

5. **Initialize Database**
```bash
sudo docker-compose exec backend python manage.py migrate
sudo docker-compose exec backend python manage.py createsuperuser
sudo docker-compose exec backend python manage.py collectstatic --noinput
```

6. **Configure Nginx (Optional but Recommended)**
```bash
sudo apt install nginx

# Create Nginx config
sudo nano /etc/nginx/sites-available/library
```

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Django Admin
    location /admin {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # Static files
    location /static {
        proxy_pass http://localhost:8000;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/library /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

7. **Configure SSL with Let's Encrypt**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### Option 2: Heroku

#### Backend (Django)

1. **Install Heroku CLI**
```bash
curl https://cli-assets.heroku.com/install.sh | sh
```

2. **Login and Create App**
```bash
cd server
heroku login
heroku create library-backend
```

3. **Add PostgreSQL**
```bash
heroku addons:create heroku-postgresql:hobby-dev
```

4. **Configure Environment**
```bash
heroku config:set DEBUG=False
heroku config:set SECRET_KEY=your-secret-key
heroku config:set ALLOWED_HOSTS=library-backend.herokuapp.com
```

5. **Deploy**
```bash
git subtree push --prefix server heroku main
# Or if using separate repos:
git push heroku main
```

6. **Initialize Database**
```bash
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

#### Frontend (Next.js on Vercel)

1. **Install Vercel CLI**
```bash
npm i -g vercel
```

2. **Deploy**
```bash
cd client
vercel --prod
```

3. **Configure Environment**
In Vercel dashboard, add:
- `NEXT_PUBLIC_API_URL`: Your Heroku backend URL

### Option 3: AWS

#### Using AWS ECS (Elastic Container Service)

1. **Push Images to ECR**
```bash
# Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

# Build and push backend
docker build -t library-backend ./server
docker tag library-backend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/library-backend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/library-backend:latest

# Build and push frontend
docker build -t library-frontend ./client
docker tag library-frontend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/library-frontend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/library-frontend:latest
```

2. **Create RDS Database**
- Use AWS Console to create MySQL RDS instance
- Note down endpoint and credentials

3. **Create ECS Task Definitions**
- Create task definition for backend
- Create task definition for frontend
- Configure environment variables

4. **Create ECS Service**
- Use Application Load Balancer
- Configure target groups for frontend and backend

### Option 4: DigitalOcean App Platform

1. **Create App**
- Connect GitHub repository
- Select "Docker Compose"

2. **Configure Components**

Backend:
- Source: `/server`
- HTTP Port: 8000
- Environment Variables: Set all required vars

Frontend:
- Source: `/client`
- HTTP Port: 3000
- Build Command: `npm run build`
- Run Command: `npm start`

Database:
- Add MySQL managed database

3. **Deploy**
- Click "Create Resources"

## 🔒 Production Checklist

### Security
- [ ] Change all default passwords
- [ ] Set strong `SECRET_KEY`
- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Set up firewall rules
- [ ] Regular security updates
- [ ] Use environment variables for secrets
- [ ] Enable rate limiting

### Performance
- [ ] Enable database query optimization
- [ ] Configure caching (Redis)
- [ ] Set up CDN for static files
- [ ] Enable Gzip compression
- [ ] Optimize images
- [ ] Configure database connection pooling
- [ ] Set up monitoring

### Backup
- [ ] Automated database backups
- [ ] File storage backups
- [ ] Backup verification
- [ ] Disaster recovery plan

### Monitoring
- [ ] Set up error tracking (Sentry)
- [ ] Configure logging
- [ ] Set up uptime monitoring
- [ ] Performance monitoring
- [ ] Database monitoring

### Documentation
- [ ] API documentation accessible
- [ ] Update README with production URLs
- [ ] Document deployment process
- [ ] Create runbooks for common issues

## 🔧 Production Environment Variables

### Backend
```bash
# Django
DEBUG=False
SECRET_KEY=<strong-random-key>
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DB_ENGINE=django.db.backends.mysql
DB_NAME=library_db
DB_USER=library_user
DB_PASSWORD=<strong-password>
DB_HOST=<database-host>
DB_PORT=3306

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# Email (optional)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=<your-email>
EMAIL_HOST_PASSWORD=<app-password>
```

### Frontend
```bash
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
```

## 📊 Monitoring & Maintenance

### Log Management
```bash
# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Rotate logs
docker-compose exec backend python manage.py clearsessions
```

### Database Backup
```bash
# Backup
docker-compose exec db mysqldump -u library_user -p library_db > backup_$(date +%Y%m%d).sql

# Restore
docker-compose exec -T db mysql -u library_user -p library_db < backup_20231218.sql
```

### Updates
```bash
# Pull latest code
git pull origin main

# Rebuild and restart
docker-compose up -d --build

# Run migrations
docker-compose exec backend python manage.py migrate
```

## 🆘 Troubleshooting

### Common Issues

1. **502 Bad Gateway**
   - Check if backend is running
   - Check nginx configuration
   - Check logs

2. **Database Connection Error**
   - Verify database credentials
   - Check if database is running
   - Check network connectivity

3. **Static Files Not Loading**
   - Run `collectstatic`
   - Check nginx configuration
   - Verify file permissions

## 📞 Support

For deployment issues:
- Check logs first
- Review this guide
- Contact DevOps team
- Create support ticket

## 🎯 Performance Optimization

### Caching
```python
# settings.py
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
    }
}
```

### Database Indexing
Already configured in models with:
- Index on title, author
- Index on ISBN
- Index on category

### CDN Configuration
- Use CloudFlare or similar
- Configure for static assets
- Enable caching

---

For additional help, refer to:
- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- [Next.js Deployment](https://nextjs.org/docs/deployment)
- [Docker Production Guide](https://docs.docker.com/compose/production/)
