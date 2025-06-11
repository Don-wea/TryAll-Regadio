import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class SensorService {

  constructor(private http: HttpClient) { }

  getHumedadActual(): Observable<any> {
    return this.http.get('http://192.168.1.90:8000/api/api/ultima_humedad/');
  }
  

}
