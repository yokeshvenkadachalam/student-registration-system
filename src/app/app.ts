import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators, ReactiveFormsModule } from '@angular/forms';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, HttpClientModule],
  template: `
    <div class="page">
      <div class="card">
        <h1>Student Registration</h1>

        <div *ngIf="showSuccess" class="alert success">
          Student added successfully! Check your email to verify.
        </div>
        <div *ngIf="errorMsg" class="alert error">
          {{ errorMsg }}
        </div>

        <form [formGroup]="studentForm" (ngSubmit)="submitForm()">
          <div class="grid">
            <label>
              First Name
              <input type="text" formControlName="first_name" />
            </label>
            <label>
              Last Name
              <input type="text" formControlName="last_name" />
            </label>
            <label>
              Email
              <input type="email" formControlName="email" />
            </label>
            <label>
              Mobile
              <input type="text" formControlName="mobile" />
            </label>
            <label>
              Gender
              <input type="text" formControlName="gender" />
            </label>
            <label>
              Current Location
              <input type="text" formControlName="current_location" />
            </label>
            <label class="col-span-2">
              Permanent Address
              <input type="text" formControlName="permanent_address" />
            </label>
            <label>
              College Name
              <input type="text" formControlName="college_name" />
            </label>
            <label>
              School Name
              <input type="text" formControlName="school_name" />
            </label>
            <label>
              Photo
              <input type="file" (change)="onFileChange($event, 'photo')" />
            </label>
            <label>
              Resume
              <input type="file" (change)="onFileChange($event, 'resume')" />
            </label>
          </div>

          <div class="actions">
            <button class="btn" type="submit">Submit</button>
          </div>
        </form>
      </div>
    </div>
  `,
  styleUrls: ['./app.css']
})
export class AppComponent {
  studentForm: FormGroup;
  showSuccess = false;
  errorMsg = '';

  constructor(private fb: FormBuilder, private http: HttpClient) {
    this.studentForm = this.fb.group({
      first_name: ['', Validators.required],
      last_name: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      mobile: ['', Validators.required],
      gender: ['', Validators.required],
      current_location: ['', Validators.required],
      permanent_address: ['', Validators.required],
      college_name: ['', Validators.required],
      school_name: ['', Validators.required],
      photo: [null, Validators.required],
      resume: [null, Validators.required]
    });
  }

  onFileChange(event: Event, field: string) {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      this.studentForm.patchValue({ [field]: input.files[0] });
    }
  }

  submitForm() {
    this.showSuccess = false;
    this.errorMsg = '';

    if (this.studentForm.invalid) {
      this.errorMsg = 'Please fill out all required fields.';
      return;
    }

    const formData = new FormData();
    Object.entries(this.studentForm.value).forEach(([key, value]) => {
      if (value !== null && value !== undefined) {
        formData.append(key, value as any);
      }
    });

    this.http.post('http://localhost:8000/students', formData).subscribe({
      next: () => {
        this.showSuccess = true;
        this.studentForm.reset();
      },
      error: (err) => {
        this.errorMsg = err.error?.detail || 'Error submitting form.';
      }
    });
  }
}
