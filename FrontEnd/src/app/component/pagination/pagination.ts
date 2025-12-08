import {Component, input, output, signal} from '@angular/core';

@Component({
  selector: 'app-pagination',
  imports: [],
  templateUrl: './pagination.html',
  styleUrl: './pagination.scss',
})
export class Pagination {

  readonly nbPages = signal<number>(1);
  readonly currentPage = input.required<number>();
  readonly changePage = output<number>()

  ngOnInit() {
    this.nbPages.set(10);
  }

  goToPage(page: number) {
    this.changePage.emit(page);
  }

  onPreviousClick() {
    if (this.currentPage() == 1) return;
    this.goToPage(this.currentPage() - 1)
  }

  onNextClick() {
    if (this.currentPage() == this.nbPages()) return;
    this.goToPage(this.currentPage() + 1)
  }

}
