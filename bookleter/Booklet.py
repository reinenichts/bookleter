import logging, shutil, sys, tempfile
from pathlib import Path, PurePath

from PyPDF2 import PdfFileWriter, PdfFileReader, pdf
from bookleter import shuffle


class Book():
    def __init__(
        self,
        input_file_path,
        start_page_number,
        end_page_number,
        direction,
        crop,
        ):

        self._validate_inputs(
            input_file_path,
            start_page_number,
            end_page_number,
            crop
        )

        current_path = Path.cwd()
        self.input_file_path = PurePath.joinpath(current_path, input_file_path)
        self.start_page_number = int(start_page_number)
        self.end_page_number = int(end_page_number)
        self.direction = direction
        self.crop = crop

        logging.basicConfig(level=logging.NOTSET)

        self.temp_path = Path(tempfile.gettempdir())

        self.original_pdf_name = self.input_file_path.name
        self.original_pdf_path = str(self.input_file_path)
        self.final_pdf_name = self.original_pdf_path.replace(".pdf", "_print_this.pdf")
        self.test_pdf_name = self.final_pdf_name.replace(".pdf", "_for_test.pdf")

    def make_booklet(self):

        page_numbers = list(range(self.start_page_number, self.end_page_number + 1))

        self.end_page_number = (self.end_page_number - self.start_page_number) + 1
        self.start_page_number = 1

        if self.end_page_number % 8 == 0:
            correct_pages_count = self.end_page_number
        else:
            correct_pages_count = ((((self.end_page_number - self.start_page_number) + 1) // 8) + 1) * 8
        blank_pages_count = correct_pages_count - self.end_page_number

        inputpdf = PdfFileReader(open(self.original_pdf_path, "rb"))
        final = PdfFileWriter()
        test_file = PdfFileWriter()

        print_order = shuffle.foop(correct_pages_count)
        test_print_order = shuffle.foop(8)

        for blank in range(blank_pages_count):
            page_numbers.append(-1)
        if self.direction == "rtl":
            page_numbers.reverse()
            test_print_order.reverse()

        for number in print_order:
            pg_number = page_numbers[number - 1]
            if pg_number == -1:
                # it's a blank page
                page = pdf.PageObject.createBlankPage(pdf=inputpdf)
                page.cropBox.lowerLeft = tuple([a + b for a, b in zip(page.cropBox.lowerLeft, (int(self.crop['left']), int(self.crop['bottom'])))])
                page.cropBox.upperRight = tuple([a - b for a, b in zip(page.cropBox.upperRight, (int(self.crop['right']), int(self.crop['top'])))])
                final.addPage(page)
            else:
                # it's a page from the original pdf
                page = inputpdf.getPage(pg_number - 1)
                # do the crops
                page.cropBox.lowerLeft = tuple([a + b for a, b in zip(page.cropBox.lowerLeft, (int(self.crop['left']), int(self.crop['bottom'])))])
                page.cropBox.upperRight = tuple([a - b for a, b in zip(page.cropBox.upperRight, (int(self.crop['right']), int(self.crop['top'])))])
                final.addPage(page)

        # if the pdf is smaller than 8 pages create no test file
        if self._get_pdf_pages_count(self.original_pdf_path) >= 8:
            for pg_number in test_print_order:
                test_file.addPage(inputpdf.getPage(pg_number - 1))
            with open(self.test_pdf_name, "wb") as output_stream:
                test_file.write(output_stream)

        with open(self.final_pdf_name, "wb") as output_stream:
            final.write(output_stream)

    def _get_pdf_pages_count(self, input_file_path):
        pdf = PdfFileReader(open(input_file_path, "rb"))
        return pdf.getNumPages()

    def _validate_inputs(
            self,
            input_file_path,
            start_page_number,
            end_page_number,
            crop
        ):
        if input_file_path == "":
            raise ValueError('Please add a pdf file')

        if "" in (start_page_number, end_page_number):
            raise ValueError('Please enter start and end page numbers')
        else:
            try:
                int(start_page_number)
                int(end_page_number)
            except:
                raise ValueError('Start and end page value must be a number')

        if int(end_page_number) > self._get_pdf_pages_count(input_file_path):
            raise ValueError('End page number out of range\nYour book has only {} pages'.format(self._get_pdf_pages_count(input_file_path)))


        crop_values = ["" for key in crop.keys() if key == crop[key]]
        if "" in crop_values:
            raise ValueError('Please enter all the crop values')
        else:
            for val in crop.values():
                try:
                    int(val)
                except:
                    raise ValueError('Crop value must be a number')

    def __str__(self):
        return str({
            "pdf_file_path": self.input_file_path,
            "start_page": self.start_page_number,
            "end_page": self.end_page_number,
            "crop": self.crop,
            "book_direction": self.direction
        })
