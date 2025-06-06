import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class SaludoService {

  apiUrl = 'http://localhost:8001/api/saludo';

  constructor(private http: HttpClient) { }

  getSaludo(): Observable<any> {
    return this.http.get<any>(this.apiUrl);
  }
  
}
