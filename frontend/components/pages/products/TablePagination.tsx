import { Pagination } from "react-headless-pagination";

interface TablePaginationProps {
  currentPage: number;
  onPageChange: (page: number) => void;
  totalPages: number;
}

export function TablePagination({
  currentPage,
  onPageChange,
  totalPages,
}: TablePaginationProps) {
  return (
    <div className="flex items-center justify-end p-4 border-t border-gray-200">
      <Pagination
        currentPage={currentPage}
        setCurrentPage={onPageChange}
        className="flex items-center gap-2"
        truncableText="..."
        truncableClassName="px-2 text-gray-500"
        totalPages={totalPages}
        edgePageCount={2}
        middlePagesSiblingCount={1}
      >
        <Pagination.PrevButton className="px-3 py-1 rounded-md border border-gray-300 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed">
          Previous
        </Pagination.PrevButton>

        <nav className="flex justify-center">
          <ul className="flex items-center gap-1">
            <Pagination.PageButton
              activeClassName="bg-blue-600 text-white border-blue-600 hover:bg-blue-700"
              inactiveClassName="text-gray-700 hover:bg-gray-50"
              className="px-3 py-1 rounded-md border border-gray-300 text-sm font-medium cursor-pointer"
            />
          </ul>
        </nav>

        <Pagination.NextButton className="px-3 py-1 rounded-md border border-gray-300 text-sm font-medium text-gray-700 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed">
          Next
        </Pagination.NextButton>
      </Pagination>
    </div>
  );
}
