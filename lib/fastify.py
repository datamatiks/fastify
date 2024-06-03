import argparse
import ast
import codecs
import functools
import operator
import os
import re
import sys
import string
from re import sub
from errors import FileExist
from textblob import TextBlob

BASE_TEMPLATES_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "templates"
)

class Fastify():
    def __init__ (self):
        pass

    def pluralize(self, name):
        blob_word = TextBlob(name)
        return blob_word.words.pluralize()[0]

    def create_model_name(self, name):
        plural = self.pluralize(name)
        plural = sub(r"(_|-)+", " ", plural).title().replace(" ", "")
        return plural

    def convert(self, name):
        """
        This function converts a underscore word  to a  Camel Case word
        """
        s1 =  re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()
        return re.sub("(.)([A-Z][a-z]+)", r"\1_\2", s1)


    def render_template_with_args_in_file(self, file, template_file_name, **kwargs):
        """
        Get a file and render the content of the template_file_name with kwargs in a file
        :param file: A File Stream to write
        :param template_file_name: path to route with template name
        :param **kwargs: Args to be rendered in template
        """
        template_file_content = "".join(
            codecs.open(template_file_name, encoding="UTF-8").readlines()
        )
        template_rendered = string.Template(template_file_content).safe_substitute(**kwargs)
        file.write(template_rendered)


    def create_or_open(self, file_name, initial_template_file_name, args):
        """
        Creates a file or open the file with file_name name
        :param file_name: String with a filename
        :param initial_template_file_name: String with path to initial template
        :param args: from console to determine path to save the files
        """
        file = None
        if not os.path.isfile(file_name):
            # If file_name does not exists, create
            file = codecs.open(file_name, "w+", encoding="UTF-8")
            print("Generating code for {}".format(file_name))
            if initial_template_file_name:
                self.render_template_with_args_in_file(file, initial_template_file_name, **{})
        else:
            # If file exists, just load the file
            print("[ERROR] File {} exist!".format(file_name))
            raise FileExist
            #file = codecs.open(file_name, "a+", encoding="UTF-8")

        return file


    def sanity_check(self, args):
        """
        Verify if the work folder is a fast api app.
        :return: None
        """
        pass

    def generic_insert_with_folder(self, 
        folder_name, file_name, template_name, args
    ):
        """
        In general if we need to put a file on a folder, we use this method
        """
        # First we make sure models are a package instead a file
        if not os.path.isdir(os.path.join(args["fast_api_app_folder"], folder_name)):
            print("Creating directory {}".format(folder_name))
            os.makedirs(os.path.join(args["fast_api_app_folder"], folder_name))
            codecs.open(
                os.path.join(args["fast_api_app_folder"], folder_name, "__init__.py"),
                "w+",
            )
        full_file_name = os.path.join(
            args["fast_api_app_folder"], folder_name, "{}.py".format(file_name)
        )
        view_file = self.create_or_open(full_file_name, "", args)

        # Load content from template
        self.render_template_with_args_in_file(
            view_file,
            os.path.join(BASE_TEMPLATES_DIR, template_name),
            model_name=args["model_name"],
            model_name_obj=args["model_name_obj"],
            model_name_obj_cap=args["model_name_obj_cap"],
            model_class_name=args["model_class_name"],
            application_name=args["fast_api_app_folder"].split("/")[-1],
        )
        view_file.close()


    def api(args):
        pass


    def execute_from_command_line(self):
        parser = argparse.ArgumentParser(
            "Create a simple CRUD Structure based Fast API application "
            "structure"
        )

        parser.add_argument("--fast_api_app_folder", default=".")

        parser.add_argument(
            "--model_name", type=str, help="Name of model for make the crud", required=True
        )

        args = vars(parser.parse_args())

        args["model_name_obj"] = args["model_name"]
        args["model_name_obj_cap"] = args["model_name_obj"].capitalize()
        args["model_class_name"] = self.create_model_name(args["model_name"])

        if args["model_name"] is not None:
            args["model_name"] = self.pluralize(args["model_name"])

        if args["fast_api_app_folder"].endswith("/"):
            args["fast_api_app_folder"] = args["fast_api_app_folder"][:-1]

        simplified_file_name = self.convert(args["model_name"].strip())

    #sanity_check(args)

        self.generic_insert_with_folder(
            "db/services", simplified_file_name, "services.py.tmpl", args
        )

        self.generic_insert_with_folder(
            "db/tables", simplified_file_name, "tables.py.tmpl", args
        )
        
        self.generic_insert_with_folder(
            "db/tables", "base_class", "db_tables_base.py.tmpl", args
        )

        self.generic_insert_with_folder(
            "db", "sessions", "db_sessions.py.tmpl", args
        )

        self.generic_insert_with_folder(
            "db", "errors", "db_errors.py.tmpl", args
        )

        self.generic_insert_with_folder(
            "schemas", simplified_file_name, "schemas.py.tmpl",args
        )

        self.generic_insert_with_folder(
            "api/routes", simplified_file_name, "routes.py.tmpl",args
        )

        self.generic_insert_with_folder(
            "api", "router", "router.py.tmpl",args
        )

        self.generic_insert_with_folder(
            ".", "main", "main_app.py.tmpl",args
        )
    

if __name__ == "__main__":
    fastify = Fastify()
    fastify.execute_from_command_line()
