import {Component, inject, input, output} from '@angular/core';
import {FormBuilder, ReactiveFormsModule, Validators} from '@angular/forms';
import {MovieFilter} from './MovieFilter';

@Component({
  selector: 'app-search-filter',
  imports: [
    ReactiveFormsModule
  ],
  templateUrl: './search-filter.html',
  styleUrl: './search-filter.scss',
})
export class SearchFilter {
  private fb = inject(FormBuilder);

  availableGenres = input.required<string[]>()
  isLoading = input.required<boolean>()

  onSearchFilter = output<MovieFilter>()

  protected filterForm = this.fb.group({
    title: ['', Validators.minLength(3)],
    genre: [''],
    year: ['']
  });

  onSubmit() {
    const { title, genre, year } = this.filterForm.value;
    const filters = {
      ...(title && { title }),
      ...(genre && { genre }),
      ...(year && { year: Number(year) })
    };
    this.onSearchFilter.emit(filters);
  }

}
