import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ControlDeFlujoComponent } from './control-de-flujo.component';

describe('ControlDeFlujoComponent', () => {
  let component: ControlDeFlujoComponent;
  let fixture: ComponentFixture<ControlDeFlujoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ControlDeFlujoComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ControlDeFlujoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
