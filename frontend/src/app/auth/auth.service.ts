import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'http://localhost:8000/api/token/';

  constructor(private http: HttpClient) {}

  login(username: string, password: string): Observable<any> {
    return this.http.post(this.apiUrl, { username, password });
  }

  isAuthenticated(): boolean {
    const token = localStorage.getItem('access_token'); // Obtiene el token del local storage
    return !!token; // Devuelve true si el token existe, false en caso contrario
  }
}
