import asyncio
from astravision_core import AstraVision

async def main():
    # Cria instância do AstraVision
    system = AstraVision("Astrasy")
    
    try:
        # Inicia o sistema de forma assíncrona
        await system.run()
    except KeyboardInterrupt:
        print("\nEncerrando AstraVision...")
    finally:
        # Limpa recursos
        system.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
