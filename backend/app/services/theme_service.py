"""
Theme Service

Contains all business logic for theme operations.
Follows the "Fat Services, Thin Routes" pattern.
"""
from typing import List, Optional, Dict, Any
from sqlalchemy.exc import IntegrityError
from app.extensions import db
from app.models.theme import Theme


class ThemeService:
    """Service class for theme business logic"""

    @staticmethod
    def get_all_themes() -> List[Dict[str, Any]]:
        """
        Get all available themes.
        
        Returns:
            List of theme dictionaries
        """
        themes = Theme.query.all()
        return [theme.to_dict() for theme in themes]

    @staticmethod
    def get_theme_by_id(theme_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific theme by ID.
        
        Args:
            theme_id: The theme ID
            
        Returns:
            Theme dictionary or None if not found
        """
        theme = Theme.query.get(theme_id)
        return theme.to_dict() if theme else None

    @staticmethod
    def create_theme(theme_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new theme.
        
        Args:
            theme_data: Dictionary containing theme information
            
        Returns:
            Created theme dictionary
            
        Raises:
            ValueError: If theme data is invalid
        """
        # Validate required fields
        if not theme_data.get('name'):
            raise ValueError("Theme name is required")

        try:
            theme = Theme(
                name=theme_data['name'],
                description=theme_data.get('description')
            )
            
            db.session.add(theme)
            db.session.commit()
            
            return theme.to_dict()
            
        except IntegrityError:
            db.session.rollback()
            raise ValueError(f"Theme with name '{theme_data['name']}' already exists")

    @staticmethod
    def update_theme(theme_id: int, theme_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update an existing theme.
        
        Args:
            theme_id: The theme ID
            theme_data: Dictionary containing updated theme information
            
        Returns:
            Updated theme dictionary or None if not found
            
        Raises:
            ValueError: If theme data is invalid
        """
        theme = Theme.query.get(theme_id)
        if not theme:
            return None

        try:
            # Update fields if provided
            if 'name' in theme_data:
                if not theme_data['name']:
                    raise ValueError("Theme name cannot be empty")
                theme.name = theme_data['name']
            
            if 'description' in theme_data:
                theme.description = theme_data['description']

            db.session.commit()
            return theme.to_dict()
            
        except IntegrityError:
            db.session.rollback()
            raise ValueError(f"Theme with name '{theme_data.get('name')}' already exists")

    @staticmethod
    def delete_theme(theme_id: int) -> bool:
        """
        Delete a theme.
        
        Args:
            theme_id: The theme ID
            
        Returns:
            True if deleted, False if not found
            
        Raises:
            ValueError: If theme is in use by users
        """
        theme = Theme.query.get(theme_id)
        if not theme:
            return False

        # Check if theme is in use
        if theme.users:
            raise ValueError(f"Cannot delete theme '{theme.name}' - it is in use by {len(theme.users)} user(s)")

        db.session.delete(theme)
        db.session.commit()
        return True

    @staticmethod
    def get_default_themes() -> List[Dict[str, Any]]:
        """
        Get list of default themes that should be created.
        
        Returns:
            List of default theme data
        """
        return [
            {
                'name': 'light-mode',
                'description': 'Clean light theme with bright colors'
            },
            {
                'name': 'dark-mode', 
                'description': 'Dark theme for low-light environments'
            },
            {
                'name': 'classic-mode',
                'description': 'Traditional golf-inspired green theme'
            },
            {
                'name': 'tron-mode',
                'description': 'Futuristic neon theme with glowing accents'
            }
        ]

    @staticmethod
    def create_default_themes() -> List[Dict[str, Any]]:
        """
        Create default themes if they don't exist.
        
        Returns:
            List of created theme dictionaries
        """
        created_themes = []
        default_themes = ThemeService.get_default_themes()
        
        for theme_data in default_themes:
            # Check if theme already exists
            existing = Theme.query.filter_by(name=theme_data['name']).first()
            if not existing:
                try:
                    created_theme = ThemeService.create_theme(theme_data)
                    created_themes.append(created_theme)
                except ValueError:
                    # Theme already exists, skip
                    pass
                    
        return created_themes 