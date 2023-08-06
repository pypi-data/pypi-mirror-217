# -*- coding: utf-8-*-

from PIL import Image
import requests
from io import BytesIO


SVG_HEADER = '<?xml version="1.0" standalone="no"?><svg width="{}" height="{}" version="1.1" xmlns="http://www.w3.org/2000/svg" style="font-family: {}; font-size:{};"><desc>Aksharify Art</desc><rect width="100%" height="100%" fill="{}"/>'
HTML_HEADER = '<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Aksharify Art</title></head><body><a href="https://primepatel.github.io/aksharify/" style="text-decoration: none">{}</a></body></html>'
SORTEDCHARS = """ `.-_',~:*;!"^/\+><r=?()|7LxtcYivTljsz[]1Jnufy{}oI#FC4VX2ehk3aZw5ASbdpqUP6%9G8mKO&0EDHg$MWRNQB@"""

def URLtoImg(url: str) -> Image:
    response = requests.get(url)
    image_data = response.content
    try:
        Image.open(BytesIO(image_data))
        return BytesIO(image_data)
    except:
        print("The provided URL does not correspond to an image.")


class AksharArt:
    
    def __init__(self, image:Image, chars:str="01") -> None:
        self.image = Image.open(image)
        self.w, self.h = self.image.size
        self.chars = list(set(chars))
        self.CH_CONSTANT = 1.78
        self.H_dis, self.V_dis = 5.55, 10
        self.font_size = 10
    
    def set_font_size(self, size: int) -> None:
        self.H_dis = (size*555)/1000
        self.V_dis = size
        self.font_size = size

    def set_dim(self, width:int=None, height:int=None) -> None:
        if width != None and height == None:
            self.w, self.h = width, int(
                (self.h/self.w * width)/self.CH_CONSTANT)
        elif width == None and height != None:
            self.w, self.h = int((self.w/self.h * height)
                                 * self.CH_CONSTANT), height
        else:
            self.w, self.h = width, height
        self.image = self.image.resize((self.w, self.h))

    def asciify(self) -> None:
        self.matrix = []
        div = 255/(len(self.chars))
        bwdata = self.image.convert('L').getdata()
        for line_no in range(self.h):
            line = []
            for pixel in range(line_no*self.w, line_no*self.w + self.w):
                line.append(self.chars[int(bwdata[pixel]/div) - 1])
            self.matrix.append(line)
    
    def replace_char(self, char:str, x:int, y:int)-> None:
        if x<self.w and y<self.h:
            self.matrix[y][x] = char
        else:
            raise IndexError

    def replace_chars(self, chars:str, x:int, y:int) -> None:
        x, y = abs(x), abs(y)
        if x>self.w or y>self.h:
            raise IndexError
        if self.w - x >= len(chars):
            for i in range(x, x + len(chars)):
                self.replace_char(
                    chars[i-x], i, y
                    )
        else:
            self.replace_chars(chars[:self.w-x], x, y)
            self.replace_chars(chars[self.w-x:], 0, y+1)

    def txt_output(self, fname:str) -> None:
        text = ""
        for line_no in range(self.h):
            text += "".join(self.matrix[line_no]) + "\n"
        with open(fname + ".txt", "w") as file:
            file.write(text)
            
    def bspan(self, char:str, char_colour:tuple) -> str:
        return f"<span style='color: rgb{char_colour};'><b>{char}</b></span>"
    
    def span(self, char:str, char_colour:tuple) -> str:
        return f"<span style='color: rgb{char_colour};'>{char}</span>"

    def tspan(self, char:str, char_color:str, x:float) -> str:
        return f'<tspan x="{x}" fill="{char_color}">{char}</tspan>'
    
    def btspan(self, char:str, char_color:str, x:float) -> str:
        return f'<tspan x="{x}" fill="{char_color}" font-weight="bold">{char}</tspan>'
    
    def rgb2hex(self, rgba:tuple) -> str:
        return '#{:02x}{:02x}{:02x}'.format(rgba[0], rgba[1], rgba[2])

    def svgify(self, bg_color:str="None", bold:bool=False) -> None:
        file = SVG_HEADER.format(
            int(self.w*self.H_dis)+41, 
            int(self.h*self.V_dis)+41,
            "monospace", self.font_size, bg_color
            )
        file += f'<a href="https://primepatel.github.io/aksharify/">'
        x, y = 20, 30
        if bold == False:
            char_func = self.tspan
        else:
            char_func = self.btspan
        for line_no in range(self.h):
            file += f'<text x="{x}" y="{y}">'
            for char_no in range(self.w):
                file += char_func(
                    f"&#{ord(self.matrix[line_no][char_no])};",
                    self.rgb2hex(self.image.getpixel((char_no, line_no))), x
                    )
                x += self.H_dis
            file += '</text>'
            x = 20
            y += self.V_dis
        file += "</a>"
        file += "</svg>"
        self.ascii_svg = file

    def htmlify(self, bold:bool=False) -> None:
        html_content = '<p style="font-size: 10px; font-family: monospace;">'
        if bold == True:
            span = self.bspan
        else:
            span = self.span
        for line_no in range(self.h):
            for char_no in range(self.w):
                html_content += span(
                    f"&#{ord(self.matrix[line_no][char_no])};", 
                    self.image.getpixel((char_no, line_no))
                    )
            html_content += '<br>'
        html_content += "</p>"
        self.ascii_html = HTML_HEADER.format(html_content)
    
    def html_output(self, fname:str) -> None:
        with open(fname + ".html", "w") as file:
            file.write(self.ascii_html)

    def svg_output(self, fname:str) -> None:
        with open(fname + ".svg", "w", encoding="utf-8-sig") as file:
            file.write(self.ascii_svg)
    
    def png_output(self, fname:str, svg2png, bg_color:str="None", height:int=None, width:int=None) -> None:
        self.svgify(bg_color)
        if height == None and width != None:
            svg2png(bytestring=self.ascii_svg,write_to=fname+'.png',output_width=width)
        elif width == None and height != None:
            svg2png(bytestring=self.ascii_svg,write_to=fname+'.png',output_height=height)
        elif height == None and width == None:
            svg2png(bytestring=self.ascii_svg, write_to=fname+'.png')
        else:
            svg2png(bytestring=self.ascii_svg,write_to=fname+'.png',output_height=height,output_width=width)


class EmojiArt(AksharArt):
    def __init__(self, image:Image, chars:str= "🙂😅") -> None:
        super().__init__(image, chars)
        self.H_dis = 20
    
    def set_font_size(self, size:float) -> None:
        self.H_dis = size
        self.V_dis = size
        self.font_size = size

class TextArt(AksharArt):
    
    def __init__(self, image:Image, chars:str=SORTEDCHARS, ordered:bool=False) -> None:
        super().__init__(image)
        self.chars = list(set(chars))
        if not ordered:
            chars = []
            for char in SORTEDCHARS:
                if char in self.chars:
                    chars.append(char)
            self.chars = chars


class NumberArt(AksharArt):

    def __init__(self, image:Image, numbers:str="0123456789") -> None:
        super().__init__(image, numbers)
        for i in self.chars:
            if not i.isnumeric():
                raise TypeError
        self.numbers = self.chars

    def numberify(self, first_num:int=0) -> None:
        self.asciify()
        if first_num != 0:
            self.matrix[0][0] = first_num

class PrimeArt(NumberArt):
    
    def __init__(self, image:Image) -> None:
        super().__init__(image, "01")
    
    def binary_to_decimal(self, binary:str) -> int:
        decimal = 0
        l = len(binary)
        for x in binary:
            l -= 1
            decimal += pow(2, l) * int(x)
        return int(decimal)
    
    # Avoid using self.asciitext
    # def primify(self, prime, asis=True, func=bin):
    #     if not asis and len(bin(int(prime))) == len(func(self.ascii_text)):
    #         self.ascii_text = func(int(prime))
    #     elif len(str(int(prime))) == len(self.ascii_text):
    #         self.ascii_text = str(prime)
    #     else:
    #         print("not primified")
