from dataclasses import dataclass
from datetime import date

@dataclass
class Transaction:
    #コントラスタ定義(要件書を見て完成させよう)
    date: date


    #リストを返す
    def to_list(self):
        return [self.date.isoformat(),
                #続きを書こう
                
                ]