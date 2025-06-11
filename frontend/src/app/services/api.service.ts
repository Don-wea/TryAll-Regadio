
import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})

export class APIService {

  apiUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) { }

  getZonas(): Observable<any> {
    return this.http.get(`${this.apiUrl}/zonas`);
  }
  
  getZona(zonaId: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/zonas/${zonaId}`);
  }

  getLecturasPorZona(zonaId: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/zonas/${zonaId}/lecturas`);
  }

  getNodosPorZona(zonaId: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/zonas/${zonaId}/nodos`);
  }

  getSensoresPorNodo(nodoId: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/nodos/${nodoId}/sensores`);
  }

  getLecturasPorSensor(sensorId: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/sensores/${sensorId}/lecturas`);
  }

}
