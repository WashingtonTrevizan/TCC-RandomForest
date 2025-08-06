#!/usr/bin/env python3
"""
🧪 SCRIPT DE TESTE PRINCIPAL
===========================

Executa todos os testes de validação do sistema:
- Testes unitários
- Testes de integração  
- Validação do pipeline completo

Uso: python run_tests.py
"""

import os
import sys
from pathlib import Path

def run_unit_tests():
    """Executa testes unitários"""
    print("🔬 EXECUTANDO TESTES UNITÁRIOS...")
    print("=" * 50)
    
    print("\n1. Validação do modelo:")
    os.system("python tests/unit/validar_modelo.py")
    
    print("\n2. Verificação de componentes:")
    os.system("python tests/unit/verificar_modelo.py")

def run_integration_tests():
    """Executa testes de integração"""
    print("\n🔗 EXECUTANDO TESTES DE INTEGRAÇÃO...")
    print("=" * 50)
    
    print("\n1. Teste completo do modelo:")
    os.system("python tests/integration/testar_modelo_realista.py")
    
    print("\n2. Teste do pipeline:")
    os.system("python tests/integration/test_pipeline.py")
    
    print("\n3. Geração de tráfego teste:")
    os.system("python tests/integration/gerar_trafego_teste.py")

def main():
    """Executa todos os testes"""
    print("🧪 SUITE COMPLETA DE TESTES")
    print("=" * 60)
    
    try:
        # Testes unitários
        run_unit_tests()
        
        # Testes de integração
        run_integration_tests()
        
        print("\n" + "=" * 60)
        print("✅ TODOS OS TESTES CONCLUÍDOS!")
        print("📊 Verifique os resultados acima para validar o sistema.")
        
    except Exception as e:
        print(f"\n❌ Erro durante execução dos testes: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
