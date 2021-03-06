'''

Copyright (C) 2016-2019 Vanessa Sochat.

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''

def main(args,parser,subparser):

    from sregistry.main import get_client
    for image in args.image:
        cli = get_client(image, quiet=args.quiet)
        cli.announce(args.command)
        response = cli.remove(image=image,
                              force=args.force)
