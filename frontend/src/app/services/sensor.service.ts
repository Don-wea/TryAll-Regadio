import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class SensorService {
  URL = 'http://192.168.1.93:8000/api/api/';
  constructor(private http: HttpClient) { }

  getHumedadActual(): Observable<any> {
    return this.http.get(this.URL + 'ultima_humedad/');
  }

  getTemperaturaActual(): Observable<any> {
    return this.http.get(this.URL + 'ultima_temperatura/');
  }
  
  getFlujoActual(): Observable<any> {
    return this.http.get(this.URL + 'ultima_flujo/');
  }

  getIDActual(): Observable<any> {
    return this.http.get(this.URL + 'ultimo_id/');
  }

}
