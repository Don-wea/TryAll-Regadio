import { CanActivate, Router } from '@angular/router';
import { Injectable } from '@angular/core';
import { AuthService } from '../auth/auth.service';

@Injectable({ providedIn: 'root', })
export class AuthGuard implements CanActivate {
  // Inyectar el servicio de autenticación y el router
  constructor(private authService: AuthService, private router: Router) { }

  // Método que se ejecuta antes de cargar una ruta
  canActivate(): boolean {
    // Si el usuario está autenticado, permitir el acceso a la ruta
    if (this.authService.isAuthenticated()) {
      return true;
    } else { 
      // Si no, redirigir al usuario a la página de inicio de sesión
      this.router.navigate(['/login']);
      return false;
    }

  }

}

@Injectable({ providedIn: 'root', })
export class AdminGuard implements CanActivate {
  // Inyectar el servicio de autenticación y el router
  constructor(private authService: AuthService, private router: Router) { }
  
  canActivate(): boolean {
    // Si el usuario es administrador, permitir el acceso a la ruta
    if (localStorage.getItem('isAdmin') === 'true') {
      return true;
    } else {
      // Si no, redirigir al usuario a la página de inicio
      this.router.navigate(['/']);
      return false;
    }

  }
}