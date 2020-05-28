import os
import subprocess
import xml.etree.ElementTree as etree
from ics import Calendar, Event
from dotenv import load_dotenv

def xml_to_ics(fp):
    c = Calendar()     
    tree = etree.parse(fp)
    root = tree.getroot()
    fields = None
    for node in root:
        for taak in node:
            fields = {f.tag: f.text for f in taak}

            # create ics event
            e = Event()
            e.name = "{} - {} ({})".format(fields["TAAK_GEBRUIKERCODE"], fields["TAAK_OMSCHRIJVING"], fields["TAAK_TAAKSOORT"])
            e.begin = fields["TAAK_BEGINDATUM"]
            e.end = fields["TAAK_EINDDATUM"]
            if "TAAK_OPMERKING" in fields.keys():
                e.description = fields["TAAK_OPMERKING"]
            
            c.events.add(e)
    return c

if __name__ == "__main__":

    # load env variables
    load_dotenv()
    job_exe = os.getenv("job_exe")
    administratie = os.getenv("administratie")
    job_num = os.getenv("job_num")
    xml_taken_file = os.getenv("xml_taken_file")
    ics_file = os.getenv("ics_file")
    
    # run job
    subprocess.call([job_exe, "EA", administratie, "JOB", job_num, "RUN"])

    # convert xml to ics
    c = xml_to_ics(xml_taken_file)
    with open(ics_file, "w") as f:
        f.write(str(c))
