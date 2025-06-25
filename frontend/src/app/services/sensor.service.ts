import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { HttpParams } from '@angular/common/http';


@Injectable({
  providedIn: 'root'
})
export class SensorService {
  URL = 'http://127.0.0.1:8000/api/';
  constructor(private http: HttpClient) { }

  getHumedadTemperaturaActual(): Observable<any> {
    return this.http.get(this.URL + 'recibir_humedad_y_temperatura/');
  }

  getHumedadActual(): Observable<any> {
    return this.http.get(this.URL + 'api/ultima_humedad/');
  }

  getTemperaturaActual(): Observable<any> {
    return this.http.get(this.URL + 'api/ultima_temperatura/');
  }
  
  getFlujoActual(): Observable<any> {
    return this.http.get(this.URL + 'recibir_flujo_actual/');
  }

  getIDActual(): Observable<any> {
    return this.http.get(this.URL + 'api/ultimo_id/');
  }

  getFlujoObjetivo(): Observable<any> {
    return this.http.get(this.URL + 'recibir_flujo/');
  }

  postFlujoObjetivo(flujo: number): Observable<any> {
    // Usa HttpParams para construir el parámetro de consulta
    const params = new HttpParams().set('cantidad_flujo', flujo.toString());
    
    return this.http.post(this.URL + 'enviar_flujo/', null, { params: params });
  }
}
