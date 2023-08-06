#
# list of util functions to build a static website after an experiment (ELN, Project, Group..) export
#
from pathlib import Path
import datetime
import pandas as pd

from stocks.models import Experiment, Project
from stocksapi.models import *

def get_experiment_export_dirname(e: Experiment) -> str:
    return e.created.strftime('%Y-%m-%d') + "_" + e.name.replace(" ", "_") + "_" + e.id


def build_static_web_site_for_eln_export(
        dir_path: Path, exp_table_path: Path, export_username:str, is_personal_export: bool,
        exported_project: Optional[Project] = None, exported_group_name: Optional[str] = None,
        exported_user: Optional[str] = None
         ):
    exp_html_table_path: Path = Path(dir_path, "eln_experiment_list.html")
    title = ""
    html_title = ""

    if is_personal_export:
        title = "My ELN"
        html_title = f"{export_username}'s ELN"
        html_title = html_title + (f" for Project <i>{exported_project.name}</i>" if exported_project else "")
        html_title = html_title + (f" in the <i>{exported_group_name}</i> Group" if exported_group_name else "")
    elif exported_project:
        # export of a project
        title = f"ELN for {exported_project.name}"
        if exported_user and not exported_group_name:
            html_title = f"{exported_user}'s experiments for Project <i>{exported_project.name}</i>"
        elif not exported_user and exported_group_name:
            html_title = f"{exported_group_name}'s experiments for Project <i>{exported_project.name}</i>"
        else:
            html_title = f"{exported_user}'s experiments for Project <i>{exported_project.name}</i>; " \
                         f"restricted to {exported_group_name} Group"
    elif exported_group_name and not exported_user:
        title = f"ELNs for {exported_group_name}"
        html_title = f"All Experiments for Group<i>{exported_group_name}</i> " \
                     f"[visible to {export_username} at export time]"
    elif exported_group_name and exported_user:
        title = f"{exported_user}'s ELN [{exported_group_name}]"
        html_title = f"All Experiments of user <i>{exported_user}</i> in Group<i>{exported_group_name}</i> " \
                     f"[visible to {export_username} at export time]"
    elif exported_user:
        title = f"{exported_user}'s ELN"
        html_title = f"All Experiments of user <i>{exported_user}</i> [visible to {export_username} at export time]"
    else:
        title = "My ELN"
        html_title = f"My Personal ELN [Filters: group=all, project=all]"

    header_html = get_html_header_for_eln_export(title)

    footer_html = get_html_footer_for_eln_export()

    df = pd.read_csv(exp_table_path, sep='\t', header=0, na_filter=False)
    df['View'] = df.apply(lambda x: _make_clickable_experiment(x['HTML'], x['PDF'], x['Experiment Live Link']), axis=1)
    df['Project'] = df.apply(lambda x: _make_clickable_project(x['Project'], x['Project Live Link']), axis=1)
    # 'Project Live Link'
    with open(exp_html_table_path, 'w', newline='') as htmlfile:
        htmlfile.write("<html>")
        htmlfile.write(header_html)
        htmlfile.write("<body>")
        htmlfile.write(f"""
        <body>
            <header id="header">
                <div class="innertube">
                    <h1>STOCKS Static ELN Export: {html_title}</h1>
                </div>
            </header>
            <div id="wrapper">
                <main>
                <div id="content">
                    <div class="innertube">
        """)
        df.to_html(htmlfile, index=False, na_rep="", table_id="experimentTable",
                   classes="table is-striped", border=0, render_links=True,
                   columns=['Name', 'Project', 'View', 'Owner', 'Group', 'Completion Status',
                            'Is Frozen', 'Summary', 'Started', 'Completed', 'Last Modified', 'Last Modified By',
                            'Frozen'], escape=False
                   )
        htmlfile.write("""
                    </div>
                </div>
                </main>
                <nav id="nav">
                    <div class="innertube">
                    <!--<h3>Menu</h3>
                        <ul>
                            <li><a href="#">Link 1</a></li>
                            <li><a href="#">Link 2</a></li>
                        </ul>-->
                    </div>
                </nav>
            </div>
        """)
        htmlfile.write(footer_html)
        htmlfile.write("</body>")
        htmlfile.write("</html>")
    htmlfile.close()

def _make_clickable_experiment(url_html, url_pdf, url_stocks):
    if not url_html and not url_pdf and not url_stocks:
        return ""
    s = "["
    if url_html:
        s = s + '<a href="{}" rel="noopener noreferrer" target="_blank">HTML</a>'.format(url_html)

    if url_pdf:
        if s != "[":
            s = s + '|'
        s = s + '<a href="{}" rel="noopener noreferrer" target="_blank">PDF</a>'.format(url_pdf)

    if url_stocks:
        if s != "[":
            s = s + '|'
        s = s + '<a href="{}" rel="noopener noreferrer" target="_blank">STOCKS</a>'.format(url_stocks)

    s = s + "]"
    return s


def _make_clickable_project(name, url_stocks):
    if not url_stocks:
        return name

    return '<a href="{}" rel="noopener noreferrer" target="_blank">{}</a>'.format(url_stocks, name)


def get_html_header_for_eln_export(title: str) -> str:
    header_scripts_html = """
        <style type="text/css">
        
                body {
                    margin:0px;
                    padding:5px;
                    font-family: Sans-Serif;
                    line-height: 1.5em;
                }
            
                #header {
                    background: #ccc;
                    height: 100px;
                }
            
                #header h1 {
                    margin: 0;
                    padding-top: 15px;
                }
            
                main {
                    padding-bottom: 10010px;
                    margin-bottom: -10000px;
                    float: left;
                    width: 100%;
                }
            
                #nav {
                    padding-bottom: 10010px;
                    margin-bottom: -10000px;
                    float: left;
                    width: 230px;
                    margin-left: -100%;
                    background: #eee;
                }
            
                #footer {
                    clear: left;
                    width: 100%;
                    background: #ccc;
                    text-align: center;
                    padding: 4px 0;
                }
    
                #wrapper {
                    overflow: hidden;
                }
                        
                #content {
                    margin-left: 230px; /* Same as 'nav' width */
                }
            
                .innertube {
                    margin: 15px; /* Padding for content */
                    margin-top: 0;
                }
        
                p {
                    color: #555;
                }
    
        
            </style>
            <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/bulma/0.9.3/css/bulma.min.css">
            <link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.13.2/css/dataTables.bulma.min.css">
            <script type="text/javascript" language="javascript" src="https://code.jquery.com/jquery-3.5.1.js"></script>
            <script type="text/javascript" language="javascript" src="https://cdn.datatables.net/1.13.2/js/jquery.dataTables.min.js"></script>
            <script type="text/javascript" language="javascript" src="https://cdn.datatables.net/1.13.2/js/dataTables.bulma.min.js"></script>
            <script type="text/javascript" class="init">
                $(document).ready( function () {
                    $('#experimentTable').DataTable();
                } );
            </script>
        """

    header_html = f"<head><title>{title}</title>" +header_scripts_html+ "</head>"
    return header_html


def get_html_footer_for_eln_export(when: datetime = datetime.now()) -> str:
    format_data = "%a %d %b %Y at %H:%M:%S"
    footer_html = f"""
        <footer id="footer">
        <div class="innertube">
            <p>Exported from STOCKS on {when.strftime(format_data)} *** EMBL Genome Biology Computational Support, {datetime.now().strftime("%Y")} *** All Rights Reserved</p>
        </div>
    </footer>
    """
    return footer_html

