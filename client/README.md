# Library Management System - Frontend

A modern, premium Next.js frontend for the Library Management System with a beautiful, professional UI.

## Features

### User Features
- 🔐 **Authentication**: Secure JWT-based authentication
- 📚 **Browse Books**: Search and filter through the book collection
- 🔍 **Advanced Search**: Filter by category, author, availability
- 📖 **Book Details**: View comprehensive book information
- 📋 **My Loans**: Track borrowed books and due dates
- 👤 **Profile Management**: Update personal information and change password
- 📱 **Responsive Design**: Works seamlessly on all devices

### Admin Features
- 📊 **Dashboard**: View library statistics
- ➕ **Book Management**: Add, edit, and delete books
- 📈 **Loan Monitoring**: Track all active loans
- 👥 **User Management**: Monitor user activities

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **Forms**: React Hook Form
- **HTTP Client**: Axios
- **Icons**: Lucide React
- **Notifications**: React Hot Toast

## Project Structure

```
client/
├── app/                    # Next.js app directory
│   ├── page.tsx           # Home page
│   ├── login/             # Login page
│   ├── register/          # Registration page
│   ├── books/             # Books browsing
│   ├── my-loans/          # User loans
│   ├── profile/           # User profile
│   ├── admin/             # Admin dashboard
│   └── layout.tsx         # Root layout
├── components/            # React components
│   ├── ui/               # Reusable UI components
│   ├── Navbar.tsx        # Navigation bar
│   ├── Footer.tsx        # Footer
│   └── BookCard.tsx      # Book card component
├── lib/                  # Utilities and services
│   ├── api.ts           # Axios configuration
│   ├── types.ts         # TypeScript types
│   ├── store.ts         # Zustand state management
│   ├── utils.ts         # Helper functions
│   ├── auth.service.ts  # Authentication API
│   ├── book.service.ts  # Books API
│   └── loan.service.ts  # Loans API
└── styles/              # Global styles
```

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Backend API running on `http://localhost:8000`

### Installation

1. **Install dependencies**:
```bash
npm install
```

2. **Set up environment variables**:
```bash
cp .env.local.example .env.local
```

Edit `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

3. **Run development server**:
```bash
npm run dev
```

4. **Open browser**:
Navigate to `http://localhost:3000`

### Build for Production

```bash
npm run build
npm start
```

## Docker Deployment

### Build and Run

```bash
docker build -t library-frontend .
docker run -p 3000:3000 -e NEXT_PUBLIC_API_URL=http://localhost:8000/api library-frontend
```

### Using Docker Compose

From the root directory:
```bash
docker-compose up -d
```

This will start:
- MySQL database on port 3306
- Django backend on port 8000
- Next.js frontend on port 3000

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `http://localhost:8000/api` |

## API Integration

The frontend integrates with the Django REST API:

- **Authentication**: `/api/auth/`
  - Register, login, profile, change password
  
- **Books**: `/api/books/`
  - List, search, filter, view details
  
- **Loans**: `/api/loans/`
  - Borrow, return, view loans

## Features Overview

### Authentication Flow
1. User registers with personal information
2. Login with username/password
3. JWT tokens stored in localStorage
4. Automatic token refresh on expiry
5. Protected routes redirect to login

### Book Browsing
- Grid layout with book cards
- Search by title, author, or ISBN
- Filter by category
- Filter by availability
- Pagination support
- View detailed book information

### Loan Management
- Borrow available books (registered users)
- View active loans
- Track due dates
- Overdue notifications
- Return books
- Fine calculation display

### Admin Dashboard
- View statistics (total books, active loans)
- Add new books with full details
- Edit existing books
- Delete books
- Monitor all loans

## UI/UX Design

### Color Scheme
- Primary: Blue (#0ea5e9)
- Success: Green
- Danger: Red
- Background: Gray-50

### Typography
- Font Family: Inter (sans-serif)
- Headings: Bold, large sizes
- Body: Regular, readable sizes

### Components
- **Cards**: Elevated with shadows, hover effects
- **Buttons**: Multiple variants (primary, secondary, danger, ghost)
- **Inputs**: Clean with focus states
- **Modals**: Centered with overlay
- **Navbar**: Sticky with responsive menu

## Browser Support

- Chrome (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)

## Performance

- Server-side rendering for initial load
- Code splitting for optimal bundle size
- Image optimization
- Lazy loading where appropriate

## Security

- JWT token authentication
- Secure password handling
- Protected API routes
- CSRF protection
- XSS prevention through React

## Future Enhancements

- [ ] Dark mode support
- [ ] Email notifications
- [ ] Book reviews and ratings
- [ ] Reading lists/wishlists
- [ ] Advanced analytics for admins
- [ ] Export reports (CSV, PDF)
- [ ] Multi-language support
- [ ] PWA features

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.

## Support

For issues and questions:
- Create an issue on GitHub
- Email: support@libraryhub.com

## Authors

- Development Team - LibraryHub
