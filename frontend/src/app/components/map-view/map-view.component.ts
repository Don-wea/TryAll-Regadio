import { Component, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import * as L from 'leaflet';
import 'leaflet-draw';

@Component({
  selector: 'app-map-view',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './map-view.component.html',
  styleUrl: './map-view.component.scss'
})
export class MapViewComponent implements AfterViewInit {

  private map!: L.Map;
  private drawnItems!: L.FeatureGroup;
  private drawControl!: L.Control.Draw;
  private polygonDrawer!: L.Draw.Polygon;

  ngAfterViewInit(): void {
    this.initMap();

    // wait a tick, then force Leaflet to resize
    setTimeout(() => {
      this.map.invalidateSize();
    }, 200);  // 200ms delay helps if some rendering/layout still in progress
  }



  private initMap(): void {
    this.map = L.map('map').setView([-34.6037, -58.3816], 13);


    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors'
    }).addTo(this.map);

    this.drawnItems = new L.FeatureGroup();
    this.map.addLayer(this.drawnItems);

    this.drawControl = new L.Control.Draw({
      edit: {
        featureGroup: this.drawnItems
      },
      draw: {
        polygon: {}, // ✅ instead of `true`
        polyline: false,
        marker: false,
        rectangle: false,
        circle: false,
        circlemarker: false
      }
    });

    this.map.addControl(this.drawControl);
    
    this.polygonDrawer = new L.Draw.Polygon(this.map as any, {});


    this.map.on(L.Draw.Event.CREATED, (event: any) => {
      const layer = event.layer;
      this.drawnItems.addLayer(layer);
      console.log('Área trazada:', layer.toGeoJSON());
    });
  }

  enableDrawPolygon(): void {
    this.polygonDrawer.enable();
  }

  clearDrawings(): void {
    this.drawnItems.clearLayers();
  }
}
