import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

// Definir interfaces para los tipos de datos que devuelve la API
export interface Humedad {
  sensor_id: string;
  zona_id: string;
  valor: number;
  unidad: string;
  fecha_hora: string;
}

export interface Temperatura {
  sensor_id: string;
  zona_id: string;
  valor: number;
  unidad: string;
  fecha_hora: string;
}

export interface Flujo {
  regador_id: string;
  zona_id: string;
  cantidad_agua_litros: number;
  energia_consumida_kwh: number;
  duracion_segundos: number;
  fecha_hora_inicio: string;
  fecha_hora_fin: string;
}

@Injectable({
  providedIn: 'root'
})
export class HistoricosService {
  private baseUrl = 'http://127.0.0.1:8000/api/datos_historicos';

  constructor(private http: HttpClient) {}

  getUltimasHumedades(cantidad: number): Observable<Humedad[]> {
    return this.http.get<Humedad[]>(`${this.baseUrl}/ultimas_humedades/${cantidad}/`);
  }

  getUltimasTemperaturas(cantidad: number): Observable<Temperatura[]> {
    return this.http.get<Temperatura[]>(`${this.baseUrl}/ultimas_temperaturas/${cantidad}/`);
  }

  getUltimosFlujos(cantidad: number): Observable<Flujo[]> {
    return this.http.get<Flujo[]>(`${this.baseUrl}/ultimos_flujos/${cantidad}/`);
  }
}
