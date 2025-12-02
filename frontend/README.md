# Wishlist App Frontend

A modern, minimalistic frontend for the Wishlist application with clean design and seamless backend integration.

## Features

- **Modern UI/UX**: Clean, minimal design with responsive layout
- **Dark/Light Mode**: Automatic theme switching based on system preference
- **Complete CRUD Operations**: Create, read, update, and delete wishlists and gifts
- **Authentication System**: Secure login, registration, and password reset
- **Public Sharing**: Share wishlists using unique tokens
- **Loading Indicators**: Visual feedback during API operations
- **Responsive Design**: Works on all device sizes

## Improvements Made

### 1. Modern Minimalist Design
- Clean, uncluttered interface with ample whitespace
- Improved color scheme with better contrast
- Consistent spacing and typography
- Smooth animations and transitions
- Responsive layout for all screen sizes

### 2. Enhanced User Experience
- Loading indicators for API operations
- Better error handling and user feedback
- Improved form validation
- Confirmation dialogs for destructive actions
- Empty state handling
- Clear visual hierarchy

### 3. Backend Integration
- Proper API error handling
- Session management with cookies
- CORS configuration for development
- Consistent data structures
- Loading states during API calls

### 4. Performance Optimizations
- Efficient DOM updates
- Optimized CSS with variables
- Minimal JavaScript bundle
- Proper event delegation

### 5. Accessibility
- Semantic HTML structure
- Proper form labels
- Sufficient color contrast
- Keyboard navigation support

## File Structure

```
frontend/
├── index.html          # Main HTML structure
├── styles.css          # Modern CSS with variables and responsive design
├── package.json        # Dependencies and build scripts
├── app.js              # Main application entry point
├── src/
│   ├── main.ts         # Main application logic
│   ├── modules/
│   │   ├── auth.ts     # Authentication module
│   │   ├── dashboard.ts # Dashboard module
│   │   └── public.ts   # Public browsing module
└── tsconfig.json       # TypeScript configuration
```

## Development

### Building the Project

```bash
# Install dependencies
npm install

# Build for production
npm run build

# Development server with hot reload
npm run dev
```

### API Integration

The frontend communicates with the backend API through the following endpoints:

- Authentication: `/api/auth/login`, `/api/auth/register`, `/api/auth/logout`
- Wishlists: `/api/wishlists`
- Gifts: `/api/gifts/wishlist/{id}`
- Public access: `/api/wishlists/token/{token}`

### Configuration

The frontend expects the backend to be available at the `/api` path. For development, ensure the backend CORS settings allow requests from the frontend origin.

## Design Philosophy

### Minimalism
- Focus on core functionality
- Remove unnecessary elements
- Use whitespace effectively
- Prioritize content over decoration

### Usability
- Intuitive navigation
- Clear visual hierarchy
- Consistent interaction patterns
- Immediate feedback for user actions

### Accessibility
- Semantic HTML structure
- Proper contrast ratios
- Keyboard navigation support
- Screen reader compatibility

## Technologies Used

- **TypeScript**: Type-safe JavaScript development
- **ESBuild**: Fast build tool
- **CSS Variables**: Consistent theming
- **Fetch API**: Modern HTTP requests
- **Modern JavaScript**: ES2020+ features

## Backend Integration

The frontend is designed to work seamlessly with the FastAPI backend. Key integration points include:

1. **Authentication**: Using session cookies for secure state management
2. **API Endpoints**: Following RESTful conventions
3. **Error Handling**: Consistent error response format
4. **CORS**: Proper cross-origin resource sharing configuration
5. **Security**: Proper headers and request validation

## Deployment

The frontend can be deployed as a static site or integrated with the backend using the provided Docker configuration. The build process creates optimized assets in the `dist/` directory.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

Please follow the existing code style and include tests for new functionality.