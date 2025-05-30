# API v1 Routes Documentation

Base URL: `/api/v1`

## Authentication

All routes except login/register require authentication via JWT token in the `Authorization` header:
```
Authorization: Bearer <jwt_token>
```

**Authentication Levels:**
- 🔓 **Public**: No authentication required
- 🔒 **User**: Valid JWT token required
- 👑 **Admin**: Valid JWT token with admin privileges required

---

## Authentication Routes (`/api/v1/auth`)

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | `/auth/login` | 🔓 | User login |
| POST | `/auth/register` | 🔓 | User registration |
| POST | `/auth/refresh` | 🔒 | Refresh JWT token |
| GET | `/auth/me` | 🔒 | Get current user info |

---

## User Routes (`/api/v1/users`) ✅

| Method | Endpoint | Auth | Description | Query Parameters |
|--------|----------|------|-------------|------------------|
| GET | `/users` | 👑 | List all users | `?search=query`, `?club_id=id`, `?is_active=true/false`, `?page=1`, `?per_page=20` |
| POST | `/users` | 👑 | Create new user | - |
| GET | `/users/{id}` | 🔒 | Get user by ID | - |
| PUT | `/users/{id}` | 🔒 | Update user | - |
| DELETE | `/users/{id}` | 👑 | Delete user (hard) | - |
| POST | `/users/{id}/deactivate` | 👑 | Deactivate user (soft) | - |
| PUT | `/users/{id}/password` | 🔒 | Update user password | - |
| GET | `/users/{id}/statistics` | 🔒 | Get user statistics | - |
| GET | `/users/search` | 🔒 | Search users | `?q=search_term`, `?limit=10` |

### User Object Structure
```json
{
  "id": 1,
  "email": "john.doe@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "full_name": "John Doe",
  "sex": "M",
  "is_active": true,
  "distance_unit": "meters",
  "timezone": "Europe/Oslo",
  "country": "Norway",
  "city": "Oslo",
  "address": "123 Golf Street",
  "postal_code": "0123",
  "full_address": "123 Golf Street, Oslo, 0123, Norway",
  "home_club_id": 1,
  "preferred_theme_id": 1,
  "current_handicap": 18.5,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z",
  "last_login": "2024-01-15T10:30:00Z"
}
```

### User Creation
```json
{
  "email": "john.doe@example.com",
  "password": "securePassword123",
  "first_name": "John",
  "last_name": "Doe",
  "sex": "M",
  "distance_unit": "meters",
  "timezone": "Europe/Oslo",
  "country": "Norway",
  "city": "Oslo",
  "address": "123 Golf Street",
  "postal_code": "0123",
  "home_club_id": 1,
  "preferred_theme_id": 1,
  "is_admin": false
}
```

### Password Update
```json
{
  "current_password": "currentPassword",
  "new_password": "newSecurePassword123",
  "confirm_password": "newSecurePassword123"
}
```

### User Statistics Response
```json
{
  "user_id": 1,
  "member_since": "2024-01-01T00:00:00Z",
  "last_login": "2024-01-15T10:30:00Z",
  "total_rounds": 25,
  "completed_rounds": 20,
  "current_handicap": 18.5,
  "home_club": "Augusta National Golf Club",
  "best_score": 82,
  "average_score": 89.5,
  "latest_differential": 15.2
}
```

---

## Theme Routes (`/api/v1/themes`)

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/themes` | 🔒 | List all themes |
| GET | `/themes/{id}` | 🔒 | Get theme by ID |
| POST | `/themes` | 👑 | Create new theme |
| PUT | `/themes/{id}` | 👑 | Update theme |
| DELETE | `/themes/{id}` | 👑 | Delete theme |
| POST | `/themes/defaults` | 👑 | Create default themes |

### Theme Object Structure
```json
{
  "id": 1,
  "name": "dark-mode",
  "description": "Dark theme for low-light environments",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

---

## Club Routes (`/api/v1/clubs`)

| Method | Endpoint | Auth | Description | Query Parameters |
|--------|----------|------|-------------|------------------|
| GET | `/clubs` | 🔒 | List all clubs | `?search=query`, `?country=name` |
| GET | `/clubs/{id}` | 🔒 | Get club by ID | `?include_courses=true` |
| POST | `/clubs` | 👑 | Create new club | - |
| PUT | `/clubs/{id}` | 👑 | Update club | - |
| DELETE | `/clubs/{id}` | 👑 | Delete club | - |
| POST | `/clubs/{id}/courses` | 👑 | Add course to club | - |

### Club Object Structure
```json
{
  "id": 1,
  "name": "Augusta National Golf Club",
  "description": "Famous golf club in Georgia",
  "website": "https://www.augusta.com",
  "email": "info@augusta.com",
  "phone": "+1-706-667-6000",
  "address": "2604 Washington Rd",
  "city": "Augusta",
  "country": "USA",
  "postal_code": "30904",
  "timezone": "US/Eastern",
  "full_address": "2604 Washington Rd, Augusta, 30904, USA",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

---

## Course Routes (`/api/v1/courses`) ✅

| Method | Endpoint | Auth | Description | Query Parameters |
|--------|----------|------|-------------|------------------|
| GET | `/courses` | 🔒 | List all courses | `?club_id=id`, `?search=query` |
| GET | `/courses/{id}` | 🔒 | Get course by ID | `?include_holes=true`, `?include_tee_sets=true`, `?full_details=true` |
| POST | `/courses` | 👑 | Create new course | - |
| PUT | `/courses/{id}` | 👑 | Update course | - |
| DELETE | `/courses/{id}` | 👑 | Delete course | - |
| PUT | `/courses/{id}/default-tee-set` | 👑 | Set default tee set | - |
| GET | `/courses/search` | 🔒 | Search courses | `?q=query` |

### Course Object Structure
```json
{
  "id": 1,
  "name": "Augusta National Golf Course",
  "holes_count": 18,
  "description": "Championship golf course",
  "club_id": 1,
  "default_tee_set_id": 1,
  "total_par": 72,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

---

## Hole Routes (`/api/v1/holes`) ✅

| Method | Endpoint | Auth | Description | Query Parameters |
|--------|----------|------|-------------|------------------|
| GET | `/holes/course/{course_id}` | 🔒 | Get holes for course | `?include_tee_positions=true` |
| GET | `/holes/{id}` | 🔒 | Get hole by ID | `?include_tee_positions=true` |
| POST | `/holes` | 👑 | Create new hole | - |
| PUT | `/holes/{id}` | 👑 | Update hole | - |
| DELETE | `/holes/{id}` | 👑 | Delete hole | - |
| POST | `/holes/standard` | 👑 | Create standard 18 holes | - |
| GET | `/holes/{id}/statistics` | 🔒 | Get hole statistics | - |
| GET | `/holes/course/{course_id}/validate` | 🔒 | Validate course holes | - |

### Hole Object Structure
```json
{
  "id": 1,
  "hole_number": 1,
  "par": 4,
  "stroke_index": 10,
  "course_id": 1,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Standard Holes Creation
```json
{
  "course_id": 1,
  "par_layout": [4,4,3,4,5,4,3,4,4,4,5,4,3,4,5,4,3,5]
}
```

---

## TeeSet Routes (`/api/v1/tee-sets`) ✅

| Method | Endpoint | Auth | Description | Query Parameters |
|--------|----------|------|-------------|------------------|
| GET | `/tee-sets/course/{course_id}` | 🔒 | Get tee sets for course | `?include_positions=true` |
| GET | `/tee-sets/{id}` | 🔒 | Get tee set by ID | `?include_positions=true` |
| POST | `/tee-sets` | 👑 | Create new tee set | - |
| PUT | `/tee-sets/{id}` | 👑 | Update tee set | - |
| DELETE | `/tee-sets/{id}` | 👑 | Delete tee set | - |
| POST | `/tee-sets/standard` | 👑 | Create standard tee sets | - |
| GET | `/tee-sets/{id}/rating` | 🔒 | Get tee set rating | `?gender=M/F` |
| GET | `/tee-sets/{id}/statistics` | 🔒 | Get tee set statistics | - |
| GET | `/tee-sets/course/{course_id}/validate` | 🔒 | Validate tee set setup | - |

### TeeSet Object Structure
```json
{
  "id": 1,
  "name": "Championship",
  "slope_rating": 130.0,
  "course_rating": 74.2,
  "women_slope_rating": 125.0,
  "women_course_rating": 70.8,
  "course_id": 1,
  "total_length_meters": 6420,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Standard TeeSet Creation
```json
{
  "course_id": 1
}
```

---

## TeePosition Routes (`/api/v1/tee-positions`) ✅

| Method | Endpoint | Auth | Description | Query Parameters |
|--------|----------|------|-------------|------------------|
| GET | `/tee-positions/tee-set/{tee_set_id}` | 🔒 | Get positions for tee set | `?unit=meters/yards` |
| GET | `/tee-positions/hole/{hole_id}` | 🔒 | Get positions for hole | `?unit=meters/yards` |
| GET | `/tee-positions/{id}` | 🔒 | Get tee position by ID | `?unit=meters/yards` |
| POST | `/tee-positions` | 👑 | Create new tee position | - |
| PUT | `/tee-positions/{id}` | 👑 | Update tee position | - |
| DELETE | `/tee-positions/{id}` | 👑 | Delete tee position | - |
| POST | `/tee-positions/bulk` | 👑 | Create bulk tee positions | - |
| POST | `/tee-positions/standard` | 👑 | Create standard distances | - |
| GET | `/tee-positions/tee-set/{tee_set_id}/statistics` | 🔒 | Get position statistics | - |
| PUT | `/tee-positions/bulk-update` | 👑 | Bulk update distances | - |

### TeePosition Object Structure
```json
{
  "id": 1,
  "length": 380,
  "length_unit": "meters",
  "length_meters": 380,
  "length_yards": 415.6,
  "hole_id": 1,
  "tee_set_id": 1,
  "hole_number": 1,
  "par": 4,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Bulk TeePosition Creation
```json
{
  "tee_set_id": 1,
  "distances": [380, 165, 420, 340, 520, 380, 155, 410, 390, 350, 545, 380, 175, 360, 495, 370, 145, 525]
}
```

### Standard Distances Creation
```json
{
  "tee_set_id": 1,
  "difficulty_level": "championship"
}
```

---

## Round Routes (`/api/v1/rounds`) ✅

| Method | Endpoint | Auth | Description | Query Parameters |
|--------|----------|------|-------------|------------------|
| GET | `/rounds/user/{user_id}` | 🔒 | Get user's rounds | `?limit=20` |
| GET | `/rounds/{id}` | 🔒 | Get round by ID | `?include_scores=true` |
| POST | `/rounds` | 🔒 | Create new round | - |
| PUT | `/rounds/{id}` | 🔒 | Update round | - |
| DELETE | `/rounds/{id}` | 🔒 | Delete round | - |
| POST | `/rounds/{id}/finalize` | 🔒 | Finalize round | - |
| GET | `/rounds/user/{user_id}/stats` | 🔒 | Get user statistics | - |

### Round Object Structure
```json
{
  "id": 1,
  "date_played": "2024-01-15",
  "handicap_used": 18.5,
  "course_handicap": 21,
  "course_rating": 72.1,
  "slope_rating": 125,
  "total_score": 89,
  "total_points": 32,
  "net_score": 68,
  "differential": 15.2,
  "is_complete": true,
  "user_id": 1,
  "course_id": 1,
  "tee_set_id": 1,
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-15T14:30:00Z"
}
```

---

## Score Routes (`/api/v1/scores`) ✅

| Method | Endpoint | Auth | Description | Query Parameters |
|--------|----------|------|-------------|------------------|
| GET | `/scores/round/{round_id}` | 🔒 | Get scores for round | - |
| GET | `/scores/{id}` | 🔒 | Get score by ID | - |
| POST | `/scores` | 🔒 | Create new score | - |
| PUT | `/scores/{id}` | 🔒 | Update score | - |
| DELETE | `/scores/{id}` | 🔒 | Delete score | - |
| POST | `/scores/bulk` | 🔒 | Create multiple scores | - |
| POST | `/scores/round/{round_id}/recalculate` | 🔒 | Recalculate points | - |

### Score Object Structure
```json
{
  "id": 1,
  "strokes": 5,
  "points": 1,
  "score_to_par": "+1",
  "score_name": "Bogey",
  "round_id": 1,
  "hole_id": 1,
  "hole_number": 1,
  "hole_par": 4,
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Bulk Score Creation
```json
{
  "round_id": 1,
  "hole_scores": [
    {"hole_number": 1, "strokes": 5},
    {"hole_number": 2, "strokes": 3},
    {"hole_number": 3, "strokes": 4}
  ]
}
```

---

## Handicap Routes (`/api/v1/handicaps`) - *Planned*

| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | `/handicaps/user/{user_id}` | 🔒 | Get user's handicap history |
| GET | `/handicaps/user/{user_id}/current` | 🔒 | Get user's current handicap |
| POST | `/handicaps` | 👑 | Create new handicap entry |
| PUT | `/handicaps/{id}` | 👑 | Update handicap entry |
| DELETE | `/handicaps/{id}` | 👑 | Delete handicap entry |
| POST | `/handicaps/initial` | 👑 | Set user's initial handicap |

### Handicap Object Structure
```json
{
  "id": 1,
  "handicap_value": 18.5,
  "start_date": "2024-01-01",
  "end_date": null,
  "reason": "Initial handicap",
  "is_current": true,
  "days_active": 45,
  "user_id": 1,
  "created_by_id": 2,
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
```

### Initial Handicap Creation
```json
{
  "user_id": 1,
  "handicap_value": 18.5,
  "reason": "Initial handicap established"
}
```

---

## Standard Response Format

### Success Response
```json
{
  "success": true,
  "data": { ... },
  "message": "Optional success message"
}
```

### Error Response
```json
{
  "success": false,
  "error": "Error type",
  "message": "Detailed error message",
  "details": { ... } // Optional validation details
}
```

### HTTP Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request (validation errors)
- `401` - Unauthorized (authentication required)
- `403` - Forbidden (insufficient privileges)
- `404` - Not Found
- `500` - Internal Server Error

---

## Development Notes

- All routes follow the "Thin Routes, Fat Services" pattern
- Business logic is in service classes (`app/services/`)
- Validation is handled by Marshmallow schemas (`app/schemas/`)
- Authentication decorators are in `app/services/auth_service.py`
- Timezone support is handled by `app/services/timezone_service.py`
- Complex temporal logic (handicaps) is in `app/services/handicap_service.py`
- Golf-specific distance calculations support both meters and yards
- TeeSet/TeePosition relationship enables flexible course configuration
- Round/Score system handles Stableford points and handicap calculations
- User management with profile data, preferences, and password management
- Automatic total calculation and differential updates

---

*Last updated: [Current Date]*
*Version: 1.5* 