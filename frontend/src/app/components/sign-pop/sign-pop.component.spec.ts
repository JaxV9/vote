import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SignPopComponent } from './sign-pop.component';

describe('SignPopComponent', () => {
  let component: SignPopComponent;
  let fixture: ComponentFixture<SignPopComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SignPopComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SignPopComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
