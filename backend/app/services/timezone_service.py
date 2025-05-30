"""
Timezone Service

Handles timezone-aware datetime operations for golf applications.
Provides utilities for converting between UTC and local times.
"""
from datetime import datetime, timezone
from typing import Optional, Union
import pytz
from zoneinfo import ZoneInfo


class TimezoneService:
    """Service for timezone-aware datetime operations"""
    
    @staticmethod
    def get_timezone(tz_name: str) -> Union[pytz.BaseTzInfo, ZoneInfo]:
        """
        Get timezone object from IANA timezone name.
        
        Args:
            tz_name: IANA timezone identifier (e.g., 'Europe/Oslo', 'US/Eastern')
            
        Returns:
            Timezone object
        """
        try:
            # Use zoneinfo for Python 3.9+ (recommended)
            return ZoneInfo(tz_name)
        except Exception:
            # Fallback to pytz for older Python versions
            return pytz.timezone(tz_name)
    
    @staticmethod
    def utc_to_local(utc_dt: datetime, tz_name: str) -> datetime:
        """
        Convert UTC datetime to local timezone.
        
        Args:
            utc_dt: UTC datetime object
            tz_name: Target timezone name
            
        Returns:
            Localized datetime
        """
        if utc_dt.tzinfo is None:
            utc_dt = utc_dt.replace(tzinfo=timezone.utc)
        
        local_tz = TimezoneService.get_timezone(tz_name)
        return utc_dt.astimezone(local_tz)
    
    @staticmethod
    def local_to_utc(local_dt: datetime, tz_name: str) -> datetime:
        """
        Convert local datetime to UTC.
        
        Args:
            local_dt: Local datetime object
            tz_name: Source timezone name
            
        Returns:
            UTC datetime
        """
        local_tz = TimezoneService.get_timezone(tz_name)
        
        if local_dt.tzinfo is None:
            local_dt = local_dt.replace(tzinfo=local_tz)
        
        return local_dt.astimezone(timezone.utc)
    
    @staticmethod
    def now_in_timezone(tz_name: str) -> datetime:
        """
        Get current datetime in specified timezone.
        
        Args:
            tz_name: Timezone name
            
        Returns:
            Current datetime in specified timezone
        """
        local_tz = TimezoneService.get_timezone(tz_name)
        return datetime.now(local_tz)
    
    @staticmethod
    def format_local_datetime(dt: datetime, tz_name: str, format_str: str = "%Y-%m-%d %H:%M:%S %Z") -> str:
        """
        Format datetime in local timezone.
        
        Args:
            dt: UTC datetime object
            tz_name: Target timezone name
            format_str: Python datetime format string
            
        Returns:
            Formatted local datetime string
        """
        local_dt = TimezoneService.utc_to_local(dt, tz_name)
        return local_dt.strftime(format_str)
    
    @staticmethod
    def get_user_timezone(user_id: int) -> str:
        """
        Get user's timezone setting.
        
        Args:
            user_id: User ID
            
        Returns:
            User's timezone name
        """
        from app.models.user import User
        user = User.query.get(user_id)
        return user.timezone if user else 'UTC'
    
    @staticmethod
    def get_club_timezone(club_id: int) -> str:
        """
        Get club's timezone setting.
        
        Args:
            club_id: Club ID
            
        Returns:
            Club's timezone name
        """
        from app.models.club import Club
        club = Club.query.get(club_id)
        return club.timezone if club else 'UTC'
    
    @staticmethod
    def get_round_timezone(round_obj) -> str:
        """
        Get appropriate timezone for a round (club timezone takes precedence).
        
        Args:
            round_obj: Round model instance
            
        Returns:
            Appropriate timezone for the round
        """
        if round_obj.course and round_obj.course.club:
            return round_obj.course.club.timezone
        elif round_obj.user:
            return round_obj.user.timezone
        return 'UTC'

    @staticmethod
    def common_norwegian_timezones():
        """Get list of common Norwegian timezones"""
        return [
            'Europe/Oslo',
            'Arctic/Longyearbyen'  # Svalbard
        ]
    
    @staticmethod
    def common_golf_timezones():
        """Get list of common golf destination timezones"""
        return [
            'Europe/Oslo',          # Norway
            'Europe/London',        # UK
            'Europe/Madrid',        # Spain
            'US/Eastern',           # US East Coast
            'US/Central',           # US Central
            'US/Mountain',          # US Mountain
            'US/Pacific',           # US West Coast
            'Australia/Sydney',     # Australia
            'Asia/Tokyo',           # Japan
            'Europe/Stockholm',     # Sweden
            'Europe/Copenhagen',    # Denmark
        ] 