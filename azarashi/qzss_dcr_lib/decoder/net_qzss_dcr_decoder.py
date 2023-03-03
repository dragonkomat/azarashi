from .qzss_dcr_decoder_base import QzssDcrDecoderBase
from .qzss_dcr_decoder import QzssDcrDecoder
from ..exception import QzssDcrDecoderException
from ..report import QzssDcReportBase


class NetQzssDcrDecoder(QzssDcrDecoderBase):
    schema = QzssDcReportBase

    def decode(self):
        if not self.sentence:
            raise EOFError('Encountered EOF')

        self.sentence = self.sentence.strip()

        if len(self.sentence) < 33:
            raise QzssDcrDecoderException(
                    'Too Short Sentence',
                    self.sentence)
        if len(self.sentence) > 33:
            raise QzssDcrDecoderException(
                    'Too Long Sentence',
                    self.sentence)

        # converts the message to bytes type
        try:
            self.message = self.sentence[1:]
        except ValueError:
            raise QzssDcrDecoderException(
                    'Invalid Message',
                    self.sentence)

        # extracts a satellite id
        self.satellite_id = self.sentence[0]
        self.satellite_prn_code = self.satellite_id | 0x80

        # generates a nmea sentence
        self.nmea = self.message_to_nmea()

        # stacks the next decoder
        return QzssDcrDecoder(**self.get_params()).decode()
