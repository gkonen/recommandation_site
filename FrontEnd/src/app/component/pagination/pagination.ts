import {Component, computed, input, output} from '@angular/core';
import {PaginationDetail} from '../../api/service/PaginationDetailModel';

@Component({
  selector: 'app-pagination',
  imports: [],
  templateUrl: './pagination.html',
  styleUrl: './pagination.scss',
})
export class Pagination {

  readonly paginationDetail = input.required<PaginationDetail>();
  readonly currentPage = computed( () => this.paginationDetail().page);
  readonly nbPages = computed(() => this.paginationDetail().total_pages);
  readonly changePage = output<number>()



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
