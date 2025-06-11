// angular
import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

//my components
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { LayoutComponent } from './components/layout/layout.component';
import { LoginComponent } from './components/login/login.component';
import { MonitoreoComponent } from './components/monitoreo/monitoreo.component';
import { TESTComponent } from './components/test/test.component';
import { MapViewComponent } from './components/map-view/map-view.component';

export const routes: Routes = [
    { path: '', redirectTo: '/monitoreo', pathMatch: 'full' },
    { path: '', component: LayoutComponent, children: [
        { path: 'dashboard', component: DashboardComponent },
        { path: 'monitoreo', component: MonitoreoComponent },
        { path: 'TEST', component: TESTComponent},
        { path: 'my-map', component: MapViewComponent },

    ]},
    { path: "login", component: LoginComponent}

];

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    exports: [RouterModule]
})

export class AppRoutingModule { }